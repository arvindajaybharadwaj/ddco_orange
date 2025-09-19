module gray_to_binary(
    input i_clk,
    input i_rst,
    input [3:0] i_gray,
    output reg [3:0] o_binary
);

    wire [3:0] w_binary;

    assign w_binary[3] = i_gray[3];
    assign w_binary[2] = w_binary[3] ^ i_gray[2];
    assign w_binary[1] = w_binary[2] ^ i_gray[1];
    assign w_binary[0] = w_binary[1] ^ i_gray[0];

    always @(posedge i_clk or posedge i_rst) begin
        if (i_rst) begin
            o_binary <= 4'b0;
        end else begin
            o_binary <= w_binary;
        end
    end

endmodule