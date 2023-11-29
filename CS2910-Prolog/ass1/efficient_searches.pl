/* 

CS2910 Assignment 1

    File: efficient_searches.pl

*/ 

/* 
 expands(+Path, ?NewNode)
 -- Path: is a list of nodes of the form Path=[Node|Nodes], where
    Node is the node we want to expand and Nodes is a list of remaining nodes already expanded and containing the root.
 -- NewNode: is a constant representing the node we want to go to, as there is an link to it from where we are currently.
*/
expands([Node|Nodes], NewNode):-
  arc(Node, NewNode),
  \+ member(NewNode, Nodes).

/* Question T2 (a) - Implementing DFS or depth-first search */
dfs(Path, Solution):-
  nth0(0,Path,X),
  goal(X),
  reverse(Path, Solution).

dfs(Path, Solution):-
  findall([NewNode|Path], expands(Path, NewNode), Expansions),
  member(Y,Expansions),
  dfs(Y, Solution).

/* Question T2 (b) - Implementing DLDFS or depth limited depth-first search */
dldfs(Path, _, Solution):-
  nth0(0,Path,X),
  goal(X),
  reverse(Path, Solution),
  !.
dldfs(Path, Limit, Solution):-
  findall([NewNode|Path], expands(Path, NewNode), Expansions),
  member(Y,Expansions),
  length(Y,Z),
  Z =< Limit,
  dldfs(Y, Limit, Solution),
  !.

/* Question T2 (c) - IDS or iterative deepening search */
ids(Path, Limit, Solution):-
  dldfs(Path, Limit, Solution),
  !.

ids(Path, Limit, Solution):-
  Limit2 is Limit+1,
  writeln(Limit2),
  ids(Path, Limit2, Solution).

/* Question T2 (d)- IDSH or iterative deepening search with history */
search_idsh(Path, Limit, History, Solution):-
  findall(DepthSolutions, dldfs(Path, Limit, DepthSolutions), NewSolution),
  \+length(NewSolution, 0),
  subset(NewSolution, History),
  reverse(History, Solution).

search_idsh(Path, Limit, History, Solution):-
  findall(DepthSolutions, dldfs(Path, Limit, DepthSolutions), NewSolution),
  \+length(NewSolution, 0),
  \+subset(NewSolution, History),
  Limit2 is Limit + 1,
  search_idsh(Path, Limit2, NewSolution, Solution).

search_idsh(Path, Limit, History, Solution):-
  Limit2 is Limit + 1,
  search_idsh(Path, Limit2, History, Solution).

idsh(Path, Limit, History, Solution):-
  search_idsh(Path, Limit, History, Solutions),
  member(Solution, Solutions).