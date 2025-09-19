module tb_binary_to_gray_simple;

    reg clk;
    reg rst;
    reg [3:0] test_binary_in;
    wire [3:0] test_gray_out;

    binary_to_gray uut (
        .i_clk(clk),
        .i_rst(rst),
        .i_binary(test_binary_in),
        .o_gray(test_gray_out)
    );

    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    initial begin
        rst = 1;
        test_binary_in = 4'b0;
        #15;
        rst = 0;
        #5;

        $display("--- Testing a few Binary to Gray values ---");

        test_binary_in = 4'b0000;
        #10;
        $display("Input Binary: %b -> Output Gray: %b", test_binary_in, test_gray_out);

        test_binary_in = 4'b0101;
        #10;
        $display("Input Binary: %b -> Output Gray: %b", test_binary_in, test_gray_out);

        test_binary_in = 4'b1011;
        #10;
        $display("Input Binary: %b -> Output Gray: %b", test_binary_in, test_gray_out);

        test_binary_in = 4'b1111;
        #10;
        $display("Input Binary: %b -> Output Gray: %b", test_binary_in, test_gray_out);

        #20;
        $finish;
    end

endmodule