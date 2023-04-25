function [DS1, DS2, DS3, DS4] = calculate_DS(kp, alpha, beta)
    % Define the transfer function
    C = tf([kp*beta kp kp*alpha],[1 0]);
    G = tf(1, [1 6 5]);
    sys = G*C/(1+G*C);

    % Get Step Input Result
    step_sys = feedback(sys, 1);
    step_info = stepinfo(step_sys);
    t = 0:0.01:20;
    y = step(sys, t);

    % Calculate the steady-state error for step input
    steady_state_value_step = y(end);
    input_mag_step = 1;

    % Get Ramp Input Result
    t = 0:0.1:10;
    ramp_input = t;
    [y, t] = lsim(sys, ramp_input, t);

    % Calculate the steady-state error for ramp input
    steady_state_value = y(end);
    input_mag = max(ramp_input);

    % Return DS1, DS2, DS3, and DS4 as outputs
    DS1 = abs(steady_state_value_step - input_mag_step)/1;
    DS2 = abs(steady_state_value - input_mag)/1;
    DS3 = step_info.Overshoot;
    DS4 = step_info.SettlingTime;
end
