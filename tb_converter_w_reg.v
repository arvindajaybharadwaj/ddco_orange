module tb_converter_with_reg;

    reg clk;
    reg [3:0] bin_in;
    reg [3:0] gray_in;
    wire [3:0] gray_out;
    wire [3:0] bin_out;
    wire [3:0] reg_gray_out;
    wire [3:0] reg_bin_out;

    binary_to_gray b2g (.bin(bin_in), .gray(gray_out));
    gray_to_binary g2b (.gray(gray_in), .bin(bin_out));

    register4 reg_g (.clk(clk), .d_in(gray_out), .q_out(reg_gray_out));
    register4 reg_b (.clk(clk), .d_in(bin_out), .q_out(reg_bin_out));

    initial clk = 0;
    always #5 clk = ~clk;  // 10ns clock period

    integer i;

    initial begin
        $display("time | bin_in | gray_out | reg_gray_out | gray_in | bin_out | reg_bin_out");
        $display("----------------------------------------------------------------------------");

        // Apply test vectors
        for (i = 0; i < 16; i = i + 1) begin
            bin_in  = i;         // feed binary values
            gray_in = i;         // also try gray values as input
            @(posedge clk);      // wait for storage
            $display("%4t |  %b  |   %b    |      %b      |   %b   |   %b   |     %b",
                     $time, bin_in, gray_out, reg_gray_out,
                     gray_in, bin_out, reg_bin_out);
        end

        $stop;
    end
endmodule