function A = to_A(edges, words)

	% now construct matrix A
	% map each row of sedge into (1,idx),(-1,idx),(1,idx)
	% and let everything else be 0
	A    = zeros(length(edges),length(words));

	for r = 1:numel(edges)
		edge = edges{r};
		edge = strsplit(edge,',');
		a1   = edge{1};
		a2   = edge{2};
		v    = edge{3};

		a1_idx = find(strcmp(words,a1));
		a2_idx = find(strcmp(words,a2));
		v_idx  = find(strcmp(words ,v));

		A(r,a1_idx) = 1 ;
		A(r,a2_idx) = -1;
		A(r,v_idx ) = 1 ;
	end
end

