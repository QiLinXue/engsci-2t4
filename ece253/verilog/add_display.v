module hier(input [4:0] sw, output [6:0] hex0);
    wire [1:0] F, R;
    // instantiate subcircuits
    mux2to1_2bit u1 (sw[1:0], sw[3:2], s2[4], F); // Multiplexer

    ha u2 (F[1], F[0], R); // Half Adder

    seg7 u3(R, hex0); // Seg7

endmodule
