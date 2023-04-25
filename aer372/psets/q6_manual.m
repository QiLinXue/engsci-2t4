%%% Define the transfer function
% kp(1+a/s) = kp s + a*kp / s
kp=45.049;
alpha=0.5;
beta=0.17;

C = tf([kp*beta kp kp*alpha],[1 0]);
G = tf(1, [1 6 5]);
sys = G*C/(1+G*C);

%%% Get Step Input Result
step_sys = feedback(sys, 1);
step_info = stepinfo(step_sys);

% Simulate the response to a step input
t = 0:0.01:20;
y = step(sys, t);

% Calculate the steady-state error
steady_state_value_step = y(end);
input_mag_step = 1;

%%% Get Ramp Input Result
% Simulate the response to the ramp input
t = 0:0.1:10;
ramp_input = t;
[y, t] = lsim(sys, ramp_input, t);

% Calculate the steady-state error
steady_state_value = y(end);
input_mag = max(ramp_input);

disp("DS1: Step SS Error="+abs(steady_state_value_step - input_mag_step)/input_mag_step)
disp("DS2: Ramp SS Error="+abs(steady_state_value - input_mag)/input_mag)
disp("DS3: Overshoot="+step_info.Overshoot)
disp("DS4: Settling time="+step_info.SettlingTime)
