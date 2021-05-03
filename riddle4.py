import itertools
import json
import logging
import string
from random import Random, random as randfloat
from typing import Iterable

import networkx as nx
from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

import config
import routes
from response import error_response

RIDDLE_4_MSG = 'the solution is buried somewhere along the paths of this graph'


@requires('authenticated')
async def info(request: Request):
    """"
    graph riddle
    """

    try:
        username = request.path_params['username']
    except KeyError:
        return error_response(f'username could not be found')

    graph = _gen_graph(username)
    graph_data = json.dumps(nx.node_link_data(graph))

    next_riddle = config.riddle_url(routes.ROUTE5)

    data = dict(
        description=RIDDLE_4_MSG,
        payload=graph_data,
        next_riddle=next_riddle,
    )

    return JSONResponse(data)


@requires('authenticated')
async def solution(request: Request):
    """"
    solution validation for graph riddle
    """

    def _verify_solution(sd: str) -> bool:
        # TODO validate solution

        return True

    try:
        try:
            data = await request.json()
            solution = data['solution']
        except json.JSONDecodeError as ex:
            # TODO improve this?
            return error_response('received malformed json')
        except KeyError:
            return error_response(
                'expected format is {"solution":"<solution>"'
            )

        if _verify_solution(solution):
            next_riddle = config.riddle_url(routes.ROUTE5)

            response_data = dict(
                solution_correct=True,
                next_riddle=next_riddle,
                # TODO piece of master key
            )
        else:
            response_data = dict(
                solution_correct=False,
                data_received=data,
            )
    except ValueError as ex:
        return error_response(str(ex))

    return JSONResponse(response_data)


def _obfuscate_graph(graph: nx.DiGraph, seed: int, **kwargs) -> nx.DiGraph:
    log = logging.getLogger('_obfuscate_graph')
    local_random = Random(seed)

    # randomize all target indices, except for the start/end indices
    solution_nodes_count = len(graph.nodes)
    log.debug(f'solution_nodes_count: {solution_nodes_count}')

    try:
        start = int(kwargs['start'])
        end = int(kwargs['end'])
    except KeyError:
        old_solution_indices = tuple(graph.nodes.keys())
    else:
        old_solution_indices = tuple(
            filter(
                lambda x: x != start or x != end,
                graph.nodes.keys()
            )
        )
    log.debug(f'old_solution_indices: {old_solution_indices}')

    new_solution_indices = tuple(
        local_random.sample(
            range(10 ** 6),
            solution_nodes_count)
    )
    randomize_mapping = dict(
        zip(
            old_solution_indices,
            new_solution_indices
        )
    )
    log.debug(f'randomize_mapping: {randomize_mapping}')
    nx.relabel_nodes(graph, randomize_mapping, copy=False)

    # create fake graph
    # all of it's edge weights have to be bigger than the number of
    # solution nodes, this guarantees a shortest path in the original nodes

    obf_nodes_count = 1000
    obf_nodes_ids = tuple(local_random.sample(range(10 ** 6), obf_nodes_count))

    def random_key():
        return local_random.choice(
            string.ascii_lowercase + string.digits + "@:/.:;"
        )

    obf_nodes = tuple(
        (
            idx,
            dict(
                key=random_key()
            )
        ) for idx in obf_nodes_ids
    )
    log.debug(f'obf_nodes: {obf_nodes}')

    obf_edges_weight_base = solution_nodes_count
    k = obf_nodes_count + solution_nodes_count
    random_target_indices = tuple(*obf_nodes_ids, *new_solution_indices)
    sources = random_target_indices
    random_targets = local_random.sample(random_target_indices, k)

    def random_weight():
        return obf_edges_weight_base * local_random.random() * obf_nodes_count

    random_weights = (
        dict(
            weight=random_weight()
        ) for _ in range(k)
    )
    obf_edges = tuple(
        zip(
            sources,
            random_targets,
            random_weights
        )
    )
    log.debug(f'obf_edges: {obf_edges}')

    obf_graph = nx.DiGraph()
    obf_graph.add_nodes_from(obf_nodes)
    obf_graph.add_weighted_edges_from(obf_edges)

    graph: nx.DiGraph = nx.compose(graph, obf_graph)

    # add some nodes/edges to the original ones, that go nowhere,
    # but have low edge weights
    dead_end_node_count = solution_nodes_count * 3
    dead_end_node_ids = tuple(
        local_random.sample(
            range(10 ** 6, 10 ** 6 + 1_000),
            dead_end_node_count
        )
    )
    for idx, source_id in enumerate(new_solution_indices):
        new_nodes = (
            (
                dead_end_node_ids[idx + i],
                dict(
                    key=random_key()
                )
            ) for i in range(3)
        )
        graph.add_nodes_from(new_nodes)
        random_weights = (
            dict(
                weight=random_weight()
            ) for _ in range(k)
        )
        sources = itertools.repeat(source_id)
        targets = obf_nodes_ids[idx:idx + 3]
        graph.add_weighted_edges_from(
            zip(
                sources,
                targets,
                random_weights
            )
        )

    log.debug(
        f'final graph: \n'
        f'nodes:{graph.nodes}\n'
        f'edges:{graph.edges}'
    )

    return graph


def _create_graph(node_data: Iterable, edge_data: Iterable) -> nx.DiGraph:
    graph = nx.DiGraph()
    solution_nodes = tuple(
        (idx, {'key': key}) for idx, key in node_data
    )
    graph.add_nodes_from(solution_nodes)
    graph.add_weighted_edges_from(edge_data)

    return graph


def _gen_graph(username: str) -> nx.DiGraph:
    log = logging.getLogger('_gen_graph')
    # TODO
    text = f'partial key #4:'

    node_indices = tuple(range(0, len(text)))
    node_data = (
        (idx, {'key': text[idx]}) for idx in node_indices
    )

    edge_data = (
        (
            source,
            target,
            randfloat()
        )
        for source, target in
        itertools.zip_longest(
            node_indices[1:],
            node_indices[:-1]
        )
    )

    graph = _create_graph(node_data, edge_data)

    seed: int = sum(map(ord, username))
    log.debug(f'seed for username {username} is {seed}')
    graph = _obfuscate_graph(graph, seed)

    return graph


ROUTES = [
    Route(
        path=f'{routes.ROUTE4}',
        endpoint=info,
        methods=['GET'],
    ),
    Route(
        path=f'{routes.ROUTE4}',
        endpoint=solution,
        methods=['POST'],
    ),
]
