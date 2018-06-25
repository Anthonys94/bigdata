alfa=0:0.1:1;
beta=alfa;
gamma=beta;
ast=[];
bst=ast;
gst=ast;
i=1;
for a = 1:10
    for b = 1:10
        for g = 1:10
            if alfa(a)+beta(b)+gamma(g)==1
                ast(i)=alfa(a);
                bst(i)=beta(b);
                gst(i)=gamma(g);
                i=i+1;
            end
        end
    end
end
comb = [ast; bst; gst];
                