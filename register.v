module register(
    input wire clk,
    input wire [3:0] d_in, 
    output wire [3:0] q_out
);

    d_flip_flop dff0(.clk(clk), .d(d_in[0]), .q(q_out[0]));
    d_flip_flop dff1(.clk(clk), .d(d_in[1]), .q(q_out[1]));
    d_flip_flop dff2(.clk(clk), .d(d_in[2]), .q(q_out[2]));
    d_flip_flop dff3(.clk(clk), .d(d_in[3]), .q(q_out[3]));
endmodule