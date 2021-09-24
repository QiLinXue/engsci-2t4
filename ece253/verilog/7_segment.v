module seg7(x, H);
    input [1:0] x;
    output [6:0] H;

    assign H[0] = ~x[1] & x[0];
    assign H[1] = 1'b0;
    assign H[2] = x[1] & ~x[0];
    assign H[3] = H[0];
    assign H[4] = x[0];
    assign H[5] = x[0]+x[1];
    assign H[6] = ~x[1];

endmodule // End of Module hello_world