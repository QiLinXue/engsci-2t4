% Transfer function for 1/(s(s^2+4s+5))
num = 1;
den = [1, 4, 5, 0];

% Create transfer function
sys = tf(num, den);

% Plot root locus
rlocus(sys);
rlocusx(sys);