# Advent of Code 2015, Day 5 -- This time in !!PowerShell!!
function main {
    $part1_strings = 0
    $part2_strings = 0

    Get-Content ./input.txt | ForEach-Object {
        # Part 1 regexes
        $has_3_vowels = ([regex]::Matches($_, "[aeiou]")).Count -ge 3
        $has_double_letter = ([regex]::Matches($_, "(.)\1+")).Count -gt 0
        $has_bad_strings = ([regex]::Matches($_, "ab|cd|pq|xy")).Count -gt 0
        $is_good_part1_string = $has_3_vowels -and $has_double_letter -and -not $has_bad_strings

        # Part 2 regexes
        $has_two_pair = ([regex]::Matches($_, "(..).*\1")).Count -gt 0
        $has_ABA_pattern = ([regex]::Matches($_, "(.).\1")).Count -gt 0
        $is_good_part2_string = $has_two_pair -and $has_ABA_pattern

        # Summing it all up
        if ($is_good_part1_string) {
            $part1_strings++
        }
        if ($is_good_part2_string) {
            $part2_strings++
        }
    }

    # Aaaaand printing it to console
    Write-Host "Part 1: $part1_strings"
    Write-Host "Part 2: $part2_strings"
}

main
