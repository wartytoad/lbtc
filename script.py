from browser import document, html
from collections import defaultdict
import sys

def prime_fac(n, search_start = 2):
    # prime factorization, in form of a dict {prime: power}
    assert (n > 0), 'Cannot prime factorize a nonpositive number.'
    if (n==1):
        return {}
    def _divide_out_all_factors(n, p):
        quotient = n
        power = 0
        while (quotient%p == 0):
            quotient /= p
            power += 1
        return (quotient, power)
    p = search_start
    while (n%p != 0 and p*p <= n):
        p+=1
    if (n%p != 0):
        return {n: 1}
    else:
        quotient, power = _divide_out_all_factors(n, p)
        pf = {p: power}
        remaining_pf = prime_fac(quotient, search_start=p+1)
        pf.update(remaining_pf)
        return pf

def stringify_pf(pf):
    prime_and_powers = list(pf.items())
    prime_and_powers.sort(key = lambda prime__: prime__[0])
    return '*'.join('%s^%s' % (prime, power) for prime, power in prime_and_powers)

def totient(pf):
    # totient of the number whose prime factorization is pf
    ans = 1
    for prime, power in pf.items():
        ans *= (prime - 1) * prime ** (power-1)
    return ans

def relatively_prime(m, pf):
    # returns if m is relatively prime to the number whose prime factorization is pf
    return all(m % prime != 0 for prime in pf.keys())

def all_divisors(n):
    pf = prime_fac(n)
    prime_power_divisors = [
        [prime ** power1 for power1 in range(0, power+1)]
        for prime, power in pf.items()
    ]
    def _product_two_lists (l1, l2):
        return [e1*e2 for e1 in l1 for e2 in l2]
    def _product_lists (lists):
        if len(lists) == 1:
            return lists[0]
        return _product_two_lists(lists[0], _product_lists(lists[1:]))
    divisors = _product_lists(prime_power_divisors)
    divisors.sort()
    return divisors

def exponentiate_mod(m, e, N):
    # compute m^e mod N
    if (e==0):
        return 1
    elif (e%2==0):
        return (exponentiate_mod(m, e/2, N) ** 2) % N
    elif (e%2==1):
        return (exponentiate_mod(m, (e-1)/2, N)**2 * m) % N
    else:
        assert False, "Shouldn't get here."

def compute_order(m, N, possible_orders):
    for order in possible_orders:
        if exponentiate_mod(m, order, N) == 1:
            return order
    else:
        assert False, "Shouldn't get here. %s %s %s" % (m, N, possible_orders)

def UKN_by_order(N,k):
    # returns elements of U_k(N) classified by order, in the form {order: [elts of that order]}
    pf = prime_fac(N)
    possible_orders = all_divisors(totient(pf))
    numbers_by_order = defaultdict(list)
    m=1
    while (m<N):
        if relatively_prime(m, pf):
            order = compute_order(m, N, possible_orders)
            numbers_by_order[order].append(m)
        m += k
    return dict(numbers_by_order)

def stringify_ints(ints_list):
    def _stringify_at_most_10_ints(ints_sublist):
        return ' '.join(str(i) for i in ints_sublist)
    if len(ints_list) <= 10:
        return _stringify_at_most_10_ints(ints_list)
    else:
        return _stringify_at_most_10_ints(ints_list[:10])+'\n'+stringify_ints(ints_list[10:])

def run(N,k,long_display):
    pf = prime_fac(N)
    output=('Prime Factorization of N: %s' % stringify_pf(pf))
    output+=('Prime Factorization of k: %s' % stringify_pf(prime_fac(k)))
    output+=('U(N) size: %s' % totient(pf))
    ukn = UKN_by_order(N, k)
    output+=('U_k(N) size: %s' % sum(len(elts) for elts in ukn.values()))
    orders = list(ukn.keys())
    orders.sort()
    for order in orders:
        elts_of_order = ukn[order]
        output+=('Order %s: %s elements.' % (order, len(elts_of_order)))
        if long_display:
            output+=(stringify_ints(elts_of_order))
    return output

def show_values(event):
    N = document["input1"].value
	k = document["input2"].value
    select = document["select"]
    long_display = select.options[select.selectedIndex].value
    output = run(N,k, long_display)
    document["zone"].clear()
    document["zone"] <= (f"Value in N field: {input1}",
    html.BR(),f"Value in k field: {input2}",
    html.BR(), f"Selected long display option: {long_display}",
    html.BR(), output
    )

document["button"].bind("click", show_values)