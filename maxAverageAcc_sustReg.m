function maxAverageAcc_sustReg(nCar,Tmax,str_save,G,B,D,nArcs)

speed_walk = 5 / 3.6;
speed_bike = 15 / 3.6;
speed_car = 25 / 3.6;

% Define parameters
arcsCar                 = find(G.Edges.Type == 1);
arcsBike                = find(G.Edges.Type == 2);
arcsWalk                = find(G.Edges.Type == 3);
arcsPT                  = find(G.Edges.Type == 4 | G.Edges.Type == 5);
nCarArcs                = sum(G.Edges.Type == 1);
Bcar                    = B(:,arcsCar);
t                       = G.Edges.Weight;

% Define variables
X                       = sdpvar(nArcs, size(D,2),'full');
xR                      = sdpvar(nCarArcs, 1,'full');
epsilon                 = sdpvar(size(D,2),1,'full');

dist_car                = sum(speed_car * (t(arcsCar)' * X(arcsCar,:))');
dist_bike               = sum(speed_bike * (t(arcsBike)' * X(arcsBike,:))');
dist_walk               = sum(speed_walk * (t(arcsWalk)' * X(arcsWalk,:))');
dist_pt                 = sum(speed_car * (t(arcsPT)' * X(arcsPT,:))');

reg_dist                = dist_car + dist_bike/50 + dist_walk/25 + dist_pt/4;

y_i                     = (t'*X)'./(sum(abs(D),1)'/2);

Cons                    = [B*X                                      == D;
                           Bcar*(sum(X(arcsCar,:),2)+xR)            == 0;
                           t(arcsCar)' * (sum(X(arcsCar,:),2)+xR)   <= nCar;
                           X                                        >= 0;
                           xR                                       >= 0;
                           epsilon                                  >= 0;
                           epsilon                                  >= (y_i-Tmax)/Tmax];

Obj                     = (epsilon.^2'*sum(abs(D),1)' + ...
                           1e-4*t'*X*ones(size(D,2),1) + ... 
                           1e-4 * reg_dist) ...
                           /sum(abs(D),"all");

options                 = sdpsettings('verbose', 1, ...
                                      'solver', 'gurobi', ...
                                      'showprogress', 1, ...
                                      'debug',1);
% options.gurobi.FeasibilityTol   = 1e-9;
% options.gurobi.OptimalityTol    = 1e-9;
% options.gurobi.BarConvTol       = 1e-9;
% options.gurobi.IntFeasTol       = 1e-9;
% options.gurobi.PSDTol           = 1e-9;
% options.gurobi.TuneTimeLimit    = 0;

sol_avgAccS             = optimize(Cons, Obj, options);
X                       = value(X);
sol_avgAccS.X           = X;
xR                      = value(xR);
xRfull                  = zeros(nArcs,1);
xRfull(arcsCar)         = xR;
sol_avgAccS.xR          = xRfull;
epsilon                 = value(epsilon);
sol_avgAccS.epsilon     = epsilon.^2;
sol_avgAccS.Obj         = value(Obj);

% Save
save(str_save,"sol_avgAccS");


end