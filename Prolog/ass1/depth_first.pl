/* 

CS2910 Assignment 1

    File: depth_first.pl

*/ 

choose(Path, Paths, RestPaths):-
  length(Paths, Length),
  nth1(Length, Paths, Path, RestPaths).
/*
 choose(+Path, +Paths, ?RestPaths).
 -- Path: is a list containing path for the search to consider.
 -- Paths: is a list of lists (paths) that we need to select the Path from.
 -- RestPaths: are the paths that remain from Paths once we select Path.
*/

combine(Expansions, RestOfPaths, NewPaths):-
  append(RestOfPaths, Expansions, NewPaths).
/*
 combine(+Expansions, +RestOfPaths, ?NewPaths).
 -- Expansions: is a list of lists containing possible new paths to consider.
 -- RestOfPaths: are the rest of the paths that need that remain unexplored.
 -- NewPaths: are the Expansions and the RestOfPaths merged. 
*/