! Day 6 2023
! Just a little fortran for fun
! Compile and run with gfortran -O3 -Wall solution.f90 -o solution && ./solution
! Runs in about 100ms on my machine, most of which is Part 2

program solution
    implicit none

    integer(kind = 8) :: race_index, num_wins, part1_score, total_times(0:3), distance_records(0:3)
    integer(kind = 8) :: total_time, distance_record
    integer, parameter :: input_unit = 10
    character(len = 64) :: line

    ! =============
    ! Input Reading
    ! =============
    open(unit = input_unit, file = 'input.txt', status = 'old')
    read(input_unit, "(A5)", advance = "no") line
    read(input_unit, *) total_times
    read(input_unit, "(A9)", advance = "no") line
    read(input_unit, *) distance_records
    close(input_unit)

    ! ======
    ! Part 1
    ! ======
    print *, "----~~~ Part 1 ~~~----"
    part1_score = 1 ! 1 is identity for multiplication
    do race_index = 0, 3
        print "(AI1)", "Race ", race_index
        num_wins = count_wins(total_times(race_index), distance_records(race_index))
        part1_score = part1_score * num_wins
        print "(A21I4)", "    Total Time: ", total_times(race_index)
        print "(A21I4)", "    Distance Record: ", distance_records(race_index)
        print "(A21I4)", "    Number of Wins: ", num_wins
    end do
    print *, ""
    print "(AI8)", "Part 1 Score: ", part1_score

    ! ======
    ! Part 2
    ! ======
    print *, "----~~~ Part 2 ~~~----"
    print "(A)", "The REAL Race"

    call int_array_to_string(total_times, line)
    read(line, *) total_time
    call int_array_to_string(distance_records, line)
    read(line, *) distance_record
    num_wins = count_wins(total_time, distance_record)

    print "(A21I16)", "    Total Time: ", total_time
    print "(A21I16)", "    Distance Record: ", distance_record
    print "(A21I16)", "    Number of Wins: ", num_wins
    print *, ""
    print "(AI8)", "Part 2 Score: ", num_wins

contains
    subroutine int_array_to_string(array, string)
        implicit none
        integer(kind = 8), intent(in) :: array(:)
        character(len = 64) :: num_string
        character(len = 64), intent(out) :: string
        integer :: index
        string = ""

        do index = 1, size(array)
            write(num_string, *) array(index)
            write(string, "(A)") trim(adjustl(string)) // trim(adjustl(num_string))
        end do
    end subroutine int_array_to_string


    function count_wins(total_time, distance_record) result(num_wins)
        implicit none
        integer(kind = 8), intent(in) :: total_time, distance_record
        integer(kind = 8) :: hold_time, num_wins, distances(0:total_time)

        num_wins = 0

        ! This is where you'd wannna do your optimizations
        ! If you spent some time on it, there's probably a way to analytically solve for the minimum / maximum
        ! feasible hold times without needing to loop over everything. That'd reduce the execution time to basically
        ! nothing
        do hold_time = 0, total_time
            distances(hold_time) = hold_time * (total_time - hold_time)
            if (distances(hold_time) > distance_record) then
                num_wins = num_wins + 1
            end if
        end do
    end function

end program solution

