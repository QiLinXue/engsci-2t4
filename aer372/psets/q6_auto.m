% Define the criteria
DS1_target = 0.01;
DS2_target = 0.28;
DS3_target = 5;
DS4_target = 1.5;

% Define the parameter ranges
kp_range = 10:1:50;
alpha_range = 0.3:0.05:0.7;
beta_range = 0.1:0.01:0.2;

% Initialize the minimum kp and the minimum DS4
min_kp = Inf;
min_alpha = Inf;
min_Beta = Inf;
% Loop over all possible combinations of kp, alpha, and beta
for kp = kp_range
    for alpha = alpha_range
        for beta = beta_range
            % Calculate the DS1, DS2, DS3, and DS4
            [DS1, DS2, DS3, DS4] = calculate_DS(kp, alpha, beta);

            % Check if the criteria are satisfied and update the minimum
            if DS1 < DS1_target && DS2 < DS2_target && DS3 < DS3_target && DS4 < DS4_target
                    if kp < min_kp
                        min_kp = kp;
                        min_alpha = alpha;
                        min_beta = beta;
                    end
            end
        end
    end
end

% Print the minimum kp and minimum DS4
if min_kp == Inf
    disp("No combination of parameters satisfies the criteria.")
else
    disp("Minimum kp!: " + min_kp)
    disp("Minimum alpha: " + min_alpha)
    disp("Minimum beta: "+ min_beta)
end

[DS1, DS2, DS3, DS4] = calculate_DS(min_kp, min_alpha, min_beta)
