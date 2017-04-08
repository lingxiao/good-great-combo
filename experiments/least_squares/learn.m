% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
% 
% Module  : Least squares formulation
% Date    : December 22nd
% Author  : Xiao Ling
% instructions: cd into cvx_2 lib
%               start matlab with:
%                 /Applications/MATLAB_R2016b.app/bin/matlab -nojvm -nosplash -nodesktop
%               cvx_begin
%               cd to current directory
%               run learn
% 
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

clc

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
% Load data
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

out_dir = '/Users/lingxiao/Documents/research/code/good-great-combo/experiments/least_squares/output/'

run_learn(out_dir)

function f = run_learn(out_dir)

	A_mat  = strcat(out_dir, 'A-matrix.txt');
	b_vec  = strcat(out_dir, 'b-vector.txt');

	A      = importdata(A_mat);
	b      = importdata(b_vec);

	[r,c]  = size(A);
	x      = zeros(c,1);

	% alternate encoding of constraints
	xx = [x;x];
	C  = [eye(c); -1*eye(c)];
	y  = ones(c*2,1);

	l =   zeros(size(x));
	u =  1*ones(size(x));

	cvx_begin
		variable x(c)
		minimize ( norm(A*x - b) )
		subject to
			C*x <= y         % round 0  adverbs   : [-1,1]
			% l <= x <= u    % round 1  adjectives: [1,1]
	cvx_end

	% Save solution for python processing
	x_out = '';

	for k = 1:length(x)
		x_out = strcat(x_out, num2str(x(k)), '\n');
	end	

	x_path  = strcat(out_dir, 'x-vector.txt')
	f       = fopen(x_path,'w');
	fprintf(f,x_out);
	fclose(f);

end





























