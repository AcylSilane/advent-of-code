! Advent of code 2015, day 2

program day2
    implicit none
    integer, dimension(3) :: input_vector
    integer :: total = 0
    integer, parameter :: input_unit = 10
    character(len=16) :: line

    open(unit=input_unit, file="input.txt", status="old")
    do while (.true.)
        read(input_unit, '(a)', end=200) line
        input_vector = parse_input(line)
        total = total + calc_wrapping_paper(input_vector(1), input_vector(2), input_vector(3))
    end do
 
200 close(input_unit)
    print *, "Part 1: ", total

contains
    pure function parse_input(line_in) result(vector)
        implicit none
        character(len=16), intent(in) :: line_in
        integer, dimension(3) :: vector
        integer :: line_length, num_start, num_end, line_index, vec_index
        line_length = len(trim(line_in))
        num_start = 1
        vec_index = 1
        do line_index = 1, line_length
            if (line_in(line_index:line_index) == "x") then
                num_end = line_index - 1
                read(line_in(num_start:num_end), "(I3)") vector(vec_index)
                num_start = line_index + 1
                vec_index = vec_index + 1
            endif
        end do
        read(line_in(num_start:line_length), "(I3)") vector(vec_index)
    end function

    pure function calc_wrapping_paper(length, width, height) result(area)
        implicit none
        integer, intent(in) :: length, width, height
        integer :: area, small1, small2

        small1 = length
        small2 = width
        if (small1 > small2) then
            small1 = width
            small2 = length
        endif
        if (height < small1) then
            small2 = small1
            small1 = height
        else if (height < small2) then
            small2 = height
        end if

        area = (2 * length * width) &
             + (2 * width * height) &
             + (2 * height * length) &
             + (small1 * small2)
    end function

end program day2
