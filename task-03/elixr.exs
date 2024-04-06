defmodule Prime do
  def is_prime(n) when n <= 1, do: false
  def is_prime(n) when is_integer(n) do
    is_prime(n, 2)
  end

  def is_prime(n, divisor) when divisor * divisor > n, do: true
  def is_prime(n, divisor) when rem(n, divisor) == 0, do: false
  def is_prime(n, divisor) do
    is_prime(n, divisor + 1)
  end

  def find_primes_up_to_n(n) when n < 2, do: []
  def find_primes_up_to_n(n) when n >= 2 do
    find_primes_up_to_n(n, 2, [])
  end

  defp find_primes_up_to_n(n, current, primes) when current > n, do: Enum.reverse(primes)
  defp find_primes_up_to_n(n, current, primes) do
    if is_prime(current) do
      find_primes_up_to_n(n, current + 1, [current | primes])
    else
      find_primes_up_to_n(n, current + 1, primes)
    end
  end
end

IO.puts("Enter a number (n): ")
input = IO.gets("") |> String.trim()  # Remove trailing newline
n = String.to_integer(input)

prime_numbers = Prime.find_primes_up_to_n(n)
IO.puts("Prime numbers up to #{n}: #{inspect(prime_numbers)}")
