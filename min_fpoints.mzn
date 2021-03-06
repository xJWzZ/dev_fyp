%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Test model for my FYP %
% Author: Jack Wall %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%DATA
% array[TEAMS,TEAMS] of int: fixtures;%Not used in this model
int: n;
set of int: TEAMS=1..n;
array[TEAMS] of int: iPoints;
% in this array[int, int], i is the opposing team and j is whether it's the first or second game.
% the output is the team number.
array[int,int] of int: games;%Games to play
array[int, int] of int: positionConstraints;

set of int: pt={0,1,3};
set of int: numberOfGames=1..(length(games) div 2);
set of int: numberOfGames0=0..(length(games) div 2);
set of int: l1={0,1};
array[TEAMS, TEAMS] of var l1: losses;
array[TEAMS] of var numberOfGames0: num_losses;

%DECISION VARIABLES
array[numberOfGames, 1..2] of var pt: points;

% I can't invert the values, so instead, I'm giving the team, 1 if their opposing team wins
% constraint forall(g in numberOfGames where games[g,1]=5\/games[g,2]=5)(
%   if games[g,1] = 5 then
%     losses[1,g] = (points[g,2] > 0)
%   else 
%     losses[1,g] = (points[g,1] > 0)
%   endif
% );

% constraint forall(j in numberOfGames where games[j,1]=1\/games[j,2]=1)(
%   if games[j,1] = 1 then
%     losses[games[j,2], 1] = (points[j,2] > 0)
%   else
%     losses[1, games[j,1]] = (points[j,1] > 0)
%   endif
% );

constraint forall(i in TEAMS)(
  num_losses[i] = sum(j in numberOfGames where i=games[j,1]\/i=games[j,2])(
    if i=games[j,1] then
      (points[j,2] > 0)
    else
      (points[j,1] > 0)
    endif
  )
);

%The addition of the points of team 1 and 2 must be a valid point assignment (0,3), (3,0) or (1,1):
constraint forall(g in numberOfGames)(
points[g,1] + points[g,2] >= 2 /\ points[g,1] + points[g,2] <= 3);

array[TEAMS] of var int: fPoints;

constraint forall(i in TEAMS)(
  fPoints[i] = iPoints[i]  + sum(j in numberOfGames where i=games[j,1]\/i=games[j,2])(
   if i=games[j,1] then
      points[j,1]
   else
      points[j,2]
   endif
   ));

array[TEAMS] of var TEAMS: finalPosition;
array[TEAMS] of var TEAMS: bestPosition;
array[TEAMS] of var TEAMS: worstPosition;

constraint forall(i,j in TEAMS)( 
  worstPosition[i]= sum(j in TEAMS)(bool2int(fPoints[j] >= fPoints[i])) 
);

%The best position of team i is given by the subtraction of the worst position and the number of teams with equal points as i.
constraint forall(i, j in TEAMS)(
  bestPosition[i] = worstPosition[i] - sum(j in TEAMS where i!=j)(bool2int(fPoints[j] == fPoints[i])) 
);

constraint forall(i in TEAMS)(finalPosition[i]>=bestPosition[i] /\  finalPosition[i]<=worstPosition[i]);

include "alldifferent.mzn";

constraint alldifferent(finalPosition);


int: numberPositionConstraints=length(positionConstraints) div 3; %Find out the number of position constraints

constraint forall(i in 1..numberPositionConstraints) (
  if positionConstraints[i,2] = 1 then
     finalPosition[positionConstraints[i,1]]=positionConstraints[i,3]
  elseif positionConstraints[i,2] = 2 then
     finalPosition[positionConstraints[i,1]]>positionConstraints[i,3]
  elseif positionConstraints[i,2] = 3 then
     finalPosition[positionConstraints[i,1]]>=positionConstraints[i,3]
  elseif positionConstraints[i,2] = 4 then
     finalPosition[positionConstraints[i,1]]<positionConstraints[i,3]
  else
     finalPosition[positionConstraints[i,1]]<=positionConstraints[i,3]  
  endif
);


% output[""];
% output["Fixtures Left=\(length(games))\n"]++
%       ["Number Of Constraints=\(length(positionConstraints)/3)\n"]++
%       ["Initial Points=\(iPoints)\n"]++
%       ["Final Positions=\(finalPosition)\n"]++
%       ["Final Points=\(fPoints)\n"]++
%       ["Losses=\(num_losses)\n"]++
%       ["FPoints=\(fPoints[1])\n"];

output["\(fPoints[1])"];

% solve satisfy;
solve minimize fPoints[1]
% solve minimize num_losses[1]
%solve minimize (p in TEAMS)(sum fPoints[p]);




