
module tb_binary_to_gray;
    reg clk;
    reg rst;
    reg [3:0] test_binary_in;
    wire [3:0] test_gray_out;

    integer infile, status, i;
    reg [3:0] bin_vec;
    reg [127:0] line;

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

        infile = $fopen("input_binary.txt", "r");
        if (infile == 0) begin
            $display("ERROR: Could not open input_binary.txt");
            $finish;
        end

        i = 0;
        while (!$feof(infile)) begin
            status = $fgets(line, infile);
            if (status) begin
                // Read 4-bit binary string
                if ($sscanf(line, "%b", bin_vec) == 1) begin
                    test_binary_in = bin_vec;
                    #10;
                    $display("Input Binary: %b -> Output Gray: %b", test_binary_in, test_gray_out);
                end
            end
            i = i + 1;
        end
        $fclose(infile);
        #10;
        $finish;
    end
endmodule