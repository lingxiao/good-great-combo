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

root = '/Users/lingxiao/Documents/research/code/good-great-ppdb/outputs/';

run_learn('iter0', root)
% run_learn('iter1a', root)
% run_learn('iter1b', root)
% run_learn('iter2a', root)
% run_learn('iter2b', root)
% run_learn('iter3a', root)
% run_learn('iter2b', root)


function f = run_learn(iter, root)

	pdir   = strcat(root, iter, '/');
	A_mat  = strcat(pdir, 'A-matrix.txt');
	b_vec  = strcat(pdir, 'b-vector.txt');

	A      = importdata(A_mat);
	b      = importdata(b_vec);

	[r,c]  = size(A);
	x      = zeros(c,1);

	% alternate encoding of constraints
	xx = [x;x];
	C  = [eye(c); -1*eye(c)];
	y  = ones(c*2,1);

	% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
	% Test on small data set
	% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

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

	x_path  = strcat(pdir, 'x-vector.txt')
	f       = fopen(x_path,'w');
	fprintf(f,x_out);
	fclose(f);

end


% adverbs = {'<close>', '<single>', '<that much>', '<other>', '<physically>', '<years>', '<just so>', '<so much>', '<still>', '<kinda>', '<generally>', '<only>', '<year>', '<completely>', '<way>', '<little>', '<no>', '<ever>', '<nothing>', '<absolutely>', '<crystal>', '<unusually>', '<the>', '<a lot>', '<long>', '<just>', '<a bit>', '<increasingly>', '<damn>', '<totally>', '<abundantly>', '<most>', '<perfectly>', '<especially>', '<slightly>', '<any>', '<far>', '<comparatively>', '<somewhat>', '<extremely>', '<particularly>', '<that>', '<rather>', '<kind of>', '<real>', '<quite>', '<a little>', '<fairly>', '<much>', '<really>', '<even>', '<relatively>', '<as>', '<more>', '<too>', '<pretty>', '<so>', '<very>'};
% for k = 1:length(adverbs)
	% run_learn(adverbs{k}, root);
% end	

































