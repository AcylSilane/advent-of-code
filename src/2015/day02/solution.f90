! Advent of code 2015, day 2

program day2
    implicit none
    integer, dimension(3) :: input_vector
    integer :: part1_total = 0
    integer :: part2_total = 0
    integer, parameter :: input_unit = 10
    character(len=16) :: line

    open(unit=input_unit, file="input.txt", status="old")
    do while (.true.)
        read(input_unit, '(a)', end=200) line
        input_vector = parse_input(line)
        part1_total = part1_total + calc_wrapping_paper(input_vector)
        part2_total = part2_total + calc_ribbon_length(input_vector)
    end do
 
200 close(input_unit)
    print *, "Part 1: ", part1_total
    print *, "Part 2: ", part2_total

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

    pure function get_smallest_sides(vec) result(result)
        implicit none
        integer, intent(in), dimension(3) :: vec
        integer, dimension(2) :: result

        result(1) = vec(1)
        result(2) = vec(2)
        if (result(1) > result(2)) then
            result(1) = vec(2)
            result(2) = vec(1)
        endif
        if (vec(3) < result(1)) then
            result(2) = result(1)
            result(1) = vec(3)
        else if (vec(3) < result(2)) then
            result(2) = vec(3)
        end if
    end function

    pure function calc_wrapping_paper(vec) result(area)
        implicit none
        integer, intent(in), dimension(3) :: vec
        integer, dimension(2) :: smallest_sides
        integer :: area
        smallest_sides = get_smallest_sides(vec)
        area = (2 * vec(1) * vec(2)) &
             + (2 * vec(2) * vec(3)) &
             + (2 * vec(3) * vec(1)) &
             + (smallest_sides(1) * smallest_sides(2))
    end function

    pure function calc_ribbon_length(vec) result(ribbon)
        implicit none
        integer, intent(in), dimension(3) :: vec
        integer, dimension(2) :: smallest_sides
        integer :: ribbon

        smallest_sides = get_smallest_sides(vec)
        ribbon = 2 * smallest_sides(1) + 2*smallest_sides(2) + calc_volume(vec)
    end function calc_ribbon_length

    pure function calc_volume(vec) result(volume)
        implicit none
        integer, intent(in), dimension(3) :: vec
        integer :: volume
        volume = vec(1) * vec(2) * vec(3)
    end function calc_volume

end program day2
