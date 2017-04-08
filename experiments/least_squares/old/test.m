% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
% 
% Module  : Least squares formulation
% Date    : December 22nd
% Author  : Xiao Ling
% Command : /Applications/MATLAB_R2016b.app/bin/matlab -nojvm -nosplash -nodesktop
% 
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

clc

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
% Load data
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

root   = '/Users/lingxiao/Documents/research/code/good-great-ppdb/outputs/';
A_mat  = strcat(root, 'A-matrix-test.txt');
b_vec  = strcat(root, 'b-vector-test.txt');

A      = importdata(A_mat);
b      = importdata(b_vec);

[r,c]  = size(A);
x      = zeros(c,1);

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
% Test on small data set
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

% try 0 - 2 since most words only get more intensified
l = -1*ones(size(x));
u =  1*ones(size(x));

cvx_begin
	variable x(c)
	minimize ( norm(A*x - b) )
	subject to
		l <= x <= u
cvx_end

% Save solution for python processing
x_out = '';

for k = 1:length(x)
	x_out = strcat(x_out, num2str(x(k)), '\n');
end	

f = fopen(strcat(root,'x-vector-test.txt'),'w');
fprintf(f,x_out);
fclose(f);




































