function o = to_labels(labels)

	ulabels = {};

	for k = 1:numel(labels)
		l = labels(k);
		l = strsplit(l{1}, '\t');

		unanimous = str2num(l{1});
		strong_1  = str2num(l{2});
		strong_2  = str2num(l{3});
		tie       = l{4};
		a_1       = l{7};
		a_2       = l{8};

		if unanimous == 3
			if strong_1 > strong_2
				ulabels{length(ulabels)+1} = {'>', a_1, a_2};
			else
				ulabels{length(ulabels)+1} = {'<', a_1, a_2};
			end
		end
	end	

	o = ulabels;
end



