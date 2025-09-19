module tb_gray_to_binary_simple;

    reg clk;
    reg rst;
    reg [3:0] test_gray_in;
    wire [3:0] test_binary_out;

    gray_to_binary uut (
        .i_clk(clk),
        .i_rst(rst),
        .i_gray(test_gray_in),
        .o_binary(test_binary_out)
    );

    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    initial begin
        rst = 1;
        test_gray_in = 4'b0;
        #15;
        rst = 0;
        #5;

        $display("--- Testing a few Gray to Binary values ---");

        test_gray_in = 4'b0000;
        #10;
        $display("Input Gray: %b -> Output Binary: %b", test_gray_in, test_binary_out);

        test_gray_in = 4'b0111;
        #10;
        $display("Input Gray: %b -> Output Binary: %b", test_gray_in, test_binary_out);

        test_gray_in = 4'b1110;
        #10;
        $display("Input Gray: %b -> Output Binary: %b", test_gray_in, test_binary_out);

        test_gray_in = 4'b1000;
        #10;
        $display("Input Gray: %b -> Output Binary: %b", test_gray_in, test_binary_out);

        #20;
        $finish;
    end

endmodule