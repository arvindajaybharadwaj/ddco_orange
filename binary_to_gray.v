module binary_to_gray(
    input i_clk,
    input i_rst,
    input [3:0] i_binary,
    output reg [3:0] o_gray
);

    wire [3:0] w_gray;

    assign w_gray[3] = i_binary[3];
    assign w_gray[2] = i_binary[3] ^ i_binary[2];
    assign w_gray[1] = i_binary[2] ^ i_binary[1];
    assign w_gray[0] = i_binary[1] ^ i_binary[0];

    always @(posedge i_clk or posedge i_rst) begin
        if (i_rst) begin
            o_gray <= 4'b0;
        end else begin
            o_gray <= w_gray;
        end
    end

endmodule