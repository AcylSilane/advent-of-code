c     Fixed-Format Fortran 77: because 72 columns is plenty!
c     And because this is oldschool, I'm gonna take advantage of the
c       historical comment syntax of "c at the start of the line"
c       instead of the more modern "! anywhere" most folks use.
c     There's also a surprise bit of obscure, weird syntax at the 
c       end of the program in the last subroutien! 

      program main
        implicit none
        integer :: x1, x2, y1, y2, plan_num
        integer, parameter :: input_unit = 10
        character(len=10) :: plan_str
        character(len=40) :: line
c       And here is probably my favorite feature of Fortran: when you
c       define an array, you can choose any arbitrary indexing scheme.
c       That lets you choose the most natural way to index stuff based
c       on whatever problem you're solving. Normally fortran is 1-based
c       but for this, 0-based makes more sense.
        logical(kind=1) :: part1_lights(0:999, 0:999) = .false.
        integer :: part2_lights(0:999, 0:999) = 0


        open(unit=input_unit, file="input.txt", status="old")
        do
          read(input_unit, '(A)', end=20) line
          call parse_line(line, plan_str, x1, y1, x2, y2)
          call update_lights(part1_lights, part2_lights,
     &                       plan_num, x1, y1, x2, y2)
        enddo
20      close(input_unit)

        print *, "Part 1: ", count(part1_lights)
        print *, "Part 2: ", sum(part2_lights)

      contains
c     ====================
c     = Find Start Index =
c     ====================
c     This function finds the index of the first ascii character 
c     inside the given range.     
c     Args:
c       line_in: The input string of interest
c       ascii_low: Lowest ascii value in the range (inclusive)
c       ascii_high: Highest ascii value in the range (inclusive)
c     Returns:
c       An integer with the index of the first char in the range
      function find_start_index(line_in,
     &                          ascii_low,
     &                          ascii_high)
     &                          result(result_idx)
        implicit none
        character(len=40), intent(in) :: line_in
        integer, intent(in) :: ascii_low, ascii_high
        character(len=1) :: char_in
        integer :: result_idx, dec_in
c       Initialize the loop
        dec_in=ichar(line_in(1:1))
        result_idx = 0
c       Search until we hit the range (or end of string)
        do while ( (dec_in < ascii_low) .or. (ascii_high < dec_in) )
          result_idx = result_idx + 1
          read(line_in(result_idx:result_idx), '(A)') char_in
          dec_in = ichar(char_in)
        enddo
      end function find_start_index

c     ============
c     = Find Num =
c     ============
c     This function finds the index of the first number in the string
c     Args:
c       line_in: The input string
c     Returns:
c       An integer with the index of the first numeric character
      function find_num(line_in) result(result_idx)
        implicit none
        character(len=40), intent(in) :: line_in
        integer :: result_idx
        integer, parameter :: ASCII_0 = 48
        integer, parameter :: ASCII_9 = 57
        result_idx = find_start_index(line_in, ASCII_0, ASCII_9)
      end function find_num

c     =============
c     = Find Char =
c     =============
c     This function finds the index of the first occurence of a char
c     Args:
c       line_in: The input string
c       query: The character to search for
c     Returns:
c       The location of the given character, or -1 if not found
      function find_char(line_in, query) result(result_idx)
        implicit none
        character(len=40), intent(in) :: line_in
        character(len=1), intent(in) :: query
        integer :: result_idx
        logical :: is_searching
        is_searching = .true.
c       Search for the character
        do result_idx=1, len(line_in)
          if (line_in(result_idx:result_idx) .eq. query) then
            is_searching = .false.
            exit
          endif
        enddo
c       If we didn't find it, return -1
        if (is_searching) then
          result_idx = -1
        endif
      end function find_char

c     ==============
c     = Parse Line =
c     ==============
c     Parses an input line and stores the results in the given variables
c     Args:
c       line_in: The input line
c       plan_str: The plan string
c       x1: The x1 coordinate
c       y1: The y1 coordinate
c       x2: The x2 coordinate
c       y2: The y2 coordinate
      subroutine parse_line(line_in, plan_str, x1, y1, x2, y2)
        implicit none
        character(len=40), intent(inout) :: line_in
        character(len=10), intent(inout) :: plan_str
        integer, intent(inout) :: x1, y1, x2, y2
        integer :: end_index
        
c       Read in the plan
        end_index = find_num(line_in)-1
        plan_str = trim(line_in(1:end_index))
        plan_num = plan_to_num(plan_str)

c       Read in X1
        line_in = line_in(end_index+1:)
        end_index = find_char(line_in, ',')-1
        read(line_in(1:end_index), "(I3)") x1
c       Read in Y1
        line_in = line_in(end_index+2:)
        end_index = find_char(line_in, ' ')-1
        read(line_in(1:end_index), "(I3)") y1

c       Read X2
        line_in = line_in(end_index+2:)
        line_in = line_in(find_num(line_in):)
        end_index = find_char(line_in, ',')-1
        read(line_in(1:end_index), "(I3)") x2
c       Read Y2
        line_in = trim(line_in(end_index+2:))
        read(line_in, "(I3)") y2
        end subroutine parse_line 

c     ===============
c     = Plan to Num =
c     ===============
c     This function maps a plan to a number
c     Args:
c       str_in: Input string. Should be one of "turn off", "toggle",
c               or "turn on"
c     Returns:
c       enumeration: A number mapped to the given plan
      function plan_to_num(str_in) result(enumeration)
        implicit none
        character(len=10), intent(in) :: str_in
        integer :: enumeration
        if (str_in .eq. "turn off") then
          enumeration = -1
        else if (str_in .eq. "toggle") then
          enumeration = 0
        else if (str_in .eq. "turn on") then
          enumeration = 1
        else
          enumeration=999
        endif
      end function plan_to_num

c     =================
c     = Update Lights =
c     =================
c     This subroutine updates the lights based on the given plan
c     Args:
c       lights: The light array
c       plan_num: The plan number
c       x1: The x1 coordinate
c       y1: The y1 coordinate
c       x2: The x2 coordinate
c       y2: The y2 coordinate
        subroutine update_lights(part1_lights, part2_lights, 
     &                           plan_num, x1, y1, x2, y2)
        implicit none
        logical(kind=1), intent(inout) :: part1_lights(:,:)
        integer, intent(inout) :: part2_lights(:,:)
        integer, intent(in) :: plan_num, x1, y1, x2, Y2
        integer :: x, y
        do x=x1, x2
          do y=y1, y2
c           And here's the punchline: an Arithmetic-If block!
c           This is sorta like a switch statement, and it has
c           has 3 cases: <1, 0, and >1. Even fortran 90 warns
c           about this being deprecated -- even back then, they
c           knew this was some confusing syntax.
c           Bonus style points for being such an odd kind of GOTO
            if (plan_num) 100, 101, 102

c             -1 = Turn off
100           part1_lights(x, y) = .false.
              part2_lights(x, y) = max(0, part2_lights(x, y)-1)
              cycle

c             0 = Toggle
101           part1_lights(x, y) = .not. part1_lights(x, y)
              part2_lights(x, y) = part2_lights(x, y) + 2
              cycle
  
c             1 = Turn on
102           part1_lights(x, y) = .true.
              part2_lights(x, y) = part2_lights(x, y) + 1
              cycle

          enddo
        enddo
        end subroutine update_lights
      end program main
