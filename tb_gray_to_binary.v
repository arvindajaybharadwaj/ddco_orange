
module tb_gray_to_binary;
    reg clk;
    reg rst;
    reg [3:0] test_gray_in;
    wire [3:0] test_binary_out;

    integer infile, status, i;
    reg [3:0] gray_vec;
    reg [127:0] line;

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

        infile = $fopen("input_gray.txt", "r");
        if (infile == 0) begin
            $display("ERROR: Could not open input_gray.txt");
            $finish;
        end

        i = 0;
        while (!$feof(infile)) begin
            status = $fgets(line, infile);
            if (status) begin
                // Read 4-bit gray string
                if ($sscanf(line, "%b", gray_vec) == 1) begin
                    test_gray_in = gray_vec;
                    #10;
                    $display("Input Gray: %b -> Output Binary: %b", test_gray_in, test_binary_out);
                end
            end
            i = i + 1;
        end
        $fclose(infile);
        #10;
        $finish;
    end
endmodule