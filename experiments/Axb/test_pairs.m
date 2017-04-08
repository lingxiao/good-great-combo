% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
% 
% Module  : Least squares formulation
% Date    : December 22nd
% Author  : Xiao Ling
% 
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

clc

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
% Load data
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

root   = '/Users/lingxiao/Documents/research/code/good-great-ppdb/outputs/';

A_path = strcat(root, 'pairs/A-valuable-worthwhile.txt');
b_path = strcat(root, 'pairs/b-valuable-worthwhile.txt');
x_path = strcat(root, 'pairs/x-valuable-worthwhile.txt');

A_mat  = strcat(root, 'A-matrix-test.txt');
run_test(A_path, b_path, x_path)

function f = run_test(A_path, b_path, x_path)

	A      = importdata(A_path);
	b      = importdata(b_path);

	[r,c]  = size(A);
	x      = zeros(c,1);

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

	f = fopen(x_path,'w');
	fprintf(f,x_out);
	fclose(f);

	end




































