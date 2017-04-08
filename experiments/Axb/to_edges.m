function o = to_edges(edges)

	adjs = {};
	advs = {};
	es   = {};

	for n = 1:numel(edges)
		edge = edges(n);
		edge = edge{1};
		edge = strsplit(edge,',');
		a1   = edge{1};
		a2   = edge{2};
		v    = edge{3};

		if not(any(ismember(a1,adjs)))
			adjs{length(adjs) + 1} = a1;
		end

		if not(any(ismember(a2,adjs)))
			adjs{length(adjs) + 1} = a2;
		end

		if not(any(ismember(v,advs)))
			advs{length(advs) + 1} = v;
		end

		es{length(es) + 1} = {a1,a2,v};
	end	

	words = {adjs{:},advs{:}};

	o = {adjs, advs, es};
end
