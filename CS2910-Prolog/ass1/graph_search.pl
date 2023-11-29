/* 

CS2910 Assignment 1

    File: graph_search.pl

*/ 

/*
 search(+Paths, -Solution).
 -- Paths: is a list of lists containing the paths currently being searched.
    e.g. If Paths = [[c,b,a],[d,b,a]], the list represents two brances of the
    tree rooted at a and shown below:
           a
           |
           b
         \/   \
        c     d
    i.e. the first element of the first list is the latest node being explored
    by the search for the path represented by that list.
 -- Solution: is a path from the initial to goal state e.g. [a,b,d], 
    where a is the initial state and d is the goal state.

 To call the search we could use a query of the form:

 ? search([[a]], S).

 where [[a]] represents the root of the tree above (initial state of search).
*/

search(Paths, Solution):-
    choose([Node|Nodes], Paths, _),
    goal(Node),
    reverse([Node|Nodes], Solution).

search(Paths, Solution):-
    choose(Path, Paths, RestOfPaths),
    findall([NewNode|Path], expands(Path, NewNode), Expansions),
    combine(Expansions, RestOfPaths, NewPaths),

search(NewPaths, Solution).
    expands([Node|_], NewNode):-
    arc(Node, NewNode).