-- Add the following statements to your testbench to
-- log the signals to a text file.
-- Format:
-- `current_sim_time time_unit: hsync vsync red green blue`
-- hsync, vsync, red, green, blue should be type `std_logic_vector`
use ieee.std_logic_textio.all;
use std.textio.all;

process(clk)
    file file_ptr: text is out "vga_out.txt";
    -- Write text to this line, then write the line to the file.
    variable line_el: line;
begin

    -- NOTE: clk frequency must be >= pixel clk frequency!
    if rising_edge(clk) then
        -- Write current sim time
        write(line_el, now); 
        write(line_el, ":"); 

        -- Write sync signals
        write(line_el, " ");
        write(line_el, hsync); 

        write(line_el, " ");
        write(line_el, vsync); 

        -- Write each color
        write(line_el, " ");
        write(line_el, red); 

        write(line_el, " ");
        write(line_el, green); 

        write(line_el, " ");
        write(line_el, blue); 

        -- Write the line to the file
        writeline(file_ptr, line_el);

    end if;
end process;
