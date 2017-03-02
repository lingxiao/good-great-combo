% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
% 
% Module  : Page rank
% Date    : Febuary 15th
% Author  : Xiao Ling
% 
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

clc

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
% 
% Load matrix and transpose so that column vector
% corresond to outgoing edges of word corresponding to that column
% 
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

root    = '/Users/lingxiao/Documents/research/code/good-great-ppdb/outputs/';
Apath   = strcat(root, 'adjacency-all-adverbs.txt');
A_trans = importdata(Apath);
A       = A_trans';

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
% 
% normalize so it's column stochastic
% 
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

normal  = sum(A.^2,1) + 1e-20;
A       = bsxfun(@rdivide,A,normal);

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
% Page rank
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 


















