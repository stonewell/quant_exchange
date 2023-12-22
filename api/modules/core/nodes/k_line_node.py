import core.node
import basic_node
import price_node

############## K Nodes, return a number to indicate a type of K line  ###########################
class KLineNode(core.node.Node):
    def __init__(self, nm):
        core.node.Node.__init__(self, nm, "K_Line")

        #register Close for notified when new value
        #we need is the price node values
        nm.register_output_wire("Close", self)

        self.clear_saved_value()

    def clear_saved_value(self):
        pass

    def consume(self, from_name, value):
        if from_name != "Close":
            return None

        p = self.nm.nodes["Price"]

        values = p.values
        vlen = len(values)

        #1.
        if (vlen >= 3 and big_raise(values[vlen - 1]) and
            cross(values[vlen - 2]) and
            big_fall(values[vlen - 3]) and
            deep_into_3(values[vlen - 1].close_price,values[vlen - 3], 0.3)):
            return 1

        #2.
        if (vlen >= 3 and big_raise(values[vlen - 1]) and
            (small_fall(values[vlen - 2]) or small_raise(values[vlen - 2])) and
            big_fall(values[vlen - 3]) and
            deep_into(values[vlen - 1].close_price, values[vlen - 3])):
            return 2

        #3.
        if (vlen >= 2 and
            (big_raise(values[vlen - 1]) or mid_raise(values[vlen - 1])) and
            big_fall(values[vlen - 2]) and
            far_from(values[vlen - 1].open_price, values[vlen - 2].close_price) and
            near_to(values[vlen - 1].close_price, values[vlen - 2].close_price)):
            return 3

        #4.
        if (vlen >= 2 and
            (big_raise(values[vlen - 1]) or mid_raise(values[vlen - 1])) and
            (big_fall(values[vlen - 2])  or mid_fall(values[vlen - 2])) and
            deep_into_3(values[vlen - 1].close_price, values[vlen - 2], 0.5)):
            return 4

        #5.
        if (vlen >= 2 and
            (big_raise(values[vlen - 1]) or mid_raise(values[vlen - 1])) and
            (big_fall(values[vlen - 2])  or mid_fall(values[vlen - 2])) and
            far_from(values[vlen - 1].open_price, values[vlen - 2].close_price) and
            far_from(values[vlen - 1].close_price, values[vlen - 2].open_price)):
            return 5

        #6.
        if (up_shadow(values[vlen - 1]) >= 2 * solid(values[vlen - 1]) and
            small_solid(values[vlen - 1]) and
            (down_shadow(values[vlen - 1]) == 0 or small_down_shadow(values[vlen - 1]))):
            return 6

        #7.
        if (down_shadow(values[vlen - 1]) >= 2 * solid(values[vlen - 1]) and
            small_solid(values[vlen - 1]) and
            (up_shadow(values[vlen - 1]) == 0 or small_up_shadow(values[vlen - 1]))):
            return 7

        #8.
        if (vlen >= 2 and
            down_shadow(values[vlen - 1]) >= solid(values[vlen - 1]) and
            down_shadow(values[vlen - 2]) >= solid(values[vlen - 2]) and
            near_to(values[vlen - 1].lowest_price, values[vlen - 2].lowest_price)):
            return 8

        #9 == 11
        if (vlen >= 3 and
            k_raise(values[vlen - 1]) and
            k_raise(values[vlen - 2]) and
            fall(values[vlen - 3]) and
            far_from(values[vlen - 2].open_price, values[vlen - 3].close_price) and
            values[vlen - 2].close_price < values[vlen - 3].close_price and
            near_to(values[vlen - 1].close_price, values[vlen - 2].close_price)):
            return 9

        #10 == 12
        if (vlen >= 5 and
            (small_raise(values[vlen - 1]) or mid_raise(values[vlen - 1])) and
            (small_raise(values[vlen - 2]) or mid_raise(values[vlen - 2])) and
            (small_raise(values[vlen - 3]) or mid_raise(values[vlen - 3])) and
            (small_raise(values[vlen - 4]) or mid_raise(values[vlen - 4])) and
            (small_raise(values[vlen - 5]) or mid_raise(values[vlen - 5]))):
            return 10

        #11 == 13
        if (vlen >= 4 and
            fall(values[vlen - 1]) and values[vlen - 1].open_price < values[vlen - 2].close_price and
            fall(values[vlen - 2]) and values[vlen - 2].open_price < values[vlen - 3].close_price and
            fall(values[vlen - 3]) and values[vlen - 3].open_price < values[vlen - 4].close_price):
            return 11

        #12 == 14
        if (vlen >= 4 and
            k_raise(values[vlen - 1]) and values[vlen - 1].close_price > values[vlen - 2].close_price and
            k_raise(values[vlen - 2]) and values[vlen - 2].close_price > values[vlen - 3].close_price and
            k_raise(values[vlen - 3]) and values[vlen - 3].close_price > values[vlen - 4].close_price):
            return 12

        #13 == 18
        if (vlen >= 5 and
            raise_or_fall_close_on_top_of_prev_close(values[vlen - 1], values[vlen - 2]) and
            raise_or_fall_close_on_top_of_prev_close(values[vlen - 2], values[vlen - 3]) and
            raise_or_fall_close_on_top_of_prev_close(values[vlen - 3], values[vlen - 4]) and
            raise_or_fall_close_on_top_of_prev_close(values[vlen - 4], values[vlen - 5])):
            return 13

        #14 == 20
        if (vlen >= 2 and
            far_from(values[vlen - 1].open_price, values[vlen - 2].close_price) and
            big_raise(values[vlen - 1])):
            return 14

        #15 == 21
        if (vlen >= 3 and
            (small_raise(values[vlen - 1]) or small_fall(values[vlen - 1]) or cross(values[vlen - 1])) and
            (small_raise(values[vlen - 2]) or small_fall(values[vlen - 2]) or cross(values[vlen - 2])) and
            (big_raise(values[vlen - 3]) or mid_raise(values[vlen - 3])) and
            (values[vlen - 1].close_price > values[vlen - 3].close_price) and
            (values[vlen - 2].close_price > values[vlen - 3].close_price)):
            return 15

        #16 == 22
        if (vlen >= 3 and
            fall(values[vlen - 1]) and
            k_raise(values[vlen - 2]) and
            values[vlen - 2].open_price > values[vlen - 3].highest_price and
            near_to(values[vlen - 1].close_price, values[vlen - 2].open_price)):
            return 16

        #17 == 23
        if (vlen >= 3 and
            k_raise(values[vlen - 1]) and
            k_raise(values[vlen - 2]) and
            values[vlen - 2].open_price > values[vlen - 3].highest_price and
            near_to(values[vlen - 1].open_price, values[vlen - 2].open_price)):
            return 17

        #18 == 24
        if (vlen >= 4 and
            fall(values[vlen - 1]) and
            fall(values[vlen - 2]) and
            fall(values[vlen - 3]) and
            values[vlen - 1].open_price < values[vlen - 4].lowest_price and
            values[vlen - 2].open_price < values[vlen - 4].lowest_price and
            values[vlen - 3].open_price < values[vlen - 4].lowest_price):
            return 18

        #19 == 25
        if (vlen >= 5 and
            (big_raise(values[vlen - 1]) or mid_raise(values[vlen - 1])) and
            fall(values[vlen - 2]) and values[vlen - 2].close_price > values[vlen - 5].open_price and
            fall(values[vlen - 3]) and values[vlen - 3].close_price > values[vlen - 5].open_price and
            fall(values[vlen - 4]) and values[vlen - 4].close_price > values[vlen - 5].open_price and
            (big_raise(values[vlen - 5]) or mid_raise(values[vlen - 5]))):
            return 19

        #20 == 27
        if (vlen >= 3 and
            (big_raise(values[vlen - 1]) or mid_raise(values[vlen - 1])) and
            (mid_fall(values[vlen - 2]) or small_fall(values[vlen - 2])) and
            (big_raise(values[vlen - 3]) or mid_raise(values[vlen - 3])) and
            values[vlen - 2].open_price < values[vlen - 1].close_price and
            values[vlen - 2].close_price > values[vlen - 1].open_price and
            values[vlen - 2].open_price < values[vlen - 3].close_price and
            values[vlen - 2].close_price > values[vlen - 3].open_price):
            return 20

        #21 == 28
        if (vlen >= 3 and
            (big_fall(values[vlen - 1]) or mid_fall(values[vlen - 1])) and
            cross(values[vlen - 2]) and
            (big_raise(values[vlen - 3]) or mid_raise(values[vlen - 3])) and
            deep_into(values[vlen - 1].close_price, values[vlen - 3])):
            return 21

        #22 == 29
        if (vlen >= 3 and
            (big_fall(values[vlen - 1]) or mid_fall(values[vlen - 1])) and
            (small_raise(values[vlen - 2]) or small_fall(values[vlen - 2])) and
            (big_raise(values[vlen - 3]) or mid_raise(values[vlen - 3])) and
            deep_into(values[vlen - 1].close_price, values[vlen - 3])):
            return 22

        #23 == 30
        if (vlen >= 2 and
            (big_fall(values[vlen - 1]) or mid_fall(values[vlen - 1])) and
            (big_raise(values[vlen - 2]) or mid_raise(values[vlen - 2])) and
            near_to(values[vlen - 1].close_price, values[vlen - 2].close_price)):
            return 23

        #24 == 31
        if (vlen >= 2 and
            (big_fall(values[vlen - 1]) or mid_fall(values[vlen - 1])) and
            (big_raise(values[vlen - 2]) or mid_raise(values[vlen - 2])) and
            (values[vlen - 1].close_price < values[vlen - 2].open_price +
            (values[vlen - 2].close_price - values[vlen - 2].open_price) / 2)):
            return 24

        #25 == 32
        if (vlen >= 2 and
            (big_fall(values[vlen - 1]) or mid_fall(values[vlen - 1])) and
            (big_raise(values[vlen - 2]) or mid_raise(values[vlen - 2])) and
            (values[vlen - 1].open_price < values[vlen - 2].close_price) and
            (values[vlen - 1].close_price < values[vlen - 2].open_price)):
            return 25

        #26 == 33
        if (vlen >= 1 and
            small_solid(values[vlen - 1]) and
            (up_shadow(values[vlen - 1]) >= solid(values[vlen - 1]) * 2) and
            (small_down_shadow(values[vlen - 1]) or down_shadow(values[vlen - 1]) == 0)):
            return 26

        #27 == 34
        if (vlen >= 1 and
            small_solid(values[vlen - 1]) and
            (down_shadow(values[vlen - 1]) >= solid(values[vlen - 1]) * 2) and
            (small_up_shadow(values[vlen - 1]) or up_shadow(values[vlen - 1]) == 0)):
            return 27

        #28 == 35
        if (vlen >= 2 and
            values[vlen - 1].highest_price == values[vlen - 2].highest_price):
            return 28

        #29 == 38
        if (vlen >= 3 and
            (mid_fall(values[vlen - 1]) or big_fall(values[vlen - 1])) and
            (mid_fall(values[vlen - 2]) or big_fall(values[vlen - 2])) and
            k_raise(values[vlen - 3]) and
            values[vlen - 2].close_price > values[vlen - 3].close_price and
            values[vlen - 2].open_price < values[vlen - 1].open_price and
            values[vlen - 2].close_price > values[vlen - 1].close_price):
            return 29

        #30 == 39
        if (vlen >= 3 and
            (mid_fall(values[vlen - 1]) or big_fall(values[vlen - 1])) and
            (mid_fall(values[vlen - 2]) or big_fall(values[vlen - 2])) and
            (mid_fall(values[vlen - 3]) or big_fall(values[vlen - 3])) and
            values[vlen - 1].open_price > values[vlen - 2].close_price and
            values[vlen - 2].open_price > values[vlen - 3].close_price):
            return 30

        #31 == 40
        if (vlen >= 6 and
            (mid_fall(values[vlen - 1]) or small_fall(values[vlen - 1])) and
            (mid_fall(values[vlen - 2]) or small_fall(values[vlen - 2])) and
            (mid_fall(values[vlen - 3]) or small_fall(values[vlen - 3])) and
            (mid_fall(values[vlen - 4]) or small_fall(values[vlen - 4])) and
            (mid_fall(values[vlen - 5]) or small_fall(values[vlen - 5])) and
            (mid_raise(values[vlen - 6]) or big_raise(values[vlen - 6]))):
            return 31

        #32 == 41
        if (vlen >= 4 and
            (mid_fall(values[vlen - 1]) or small_fall(values[vlen - 1])) and
            (values[vlen - 1].close_price < values[vlen - 2].open_price + solid(values[vlen - 2]) / 2) and
            (mid_raise(values[vlen - 2]) or small_raise(values[vlen - 2])) and
            (solid(values[vlen - 2]) < solid(values[vlen - 3])) and
            (mid_fall(values[vlen - 3]) or big_fall(values[vlen - 3])) and
            (values[vlen - 3].open_price > values[vlen - 4].close_price) and
            (values[vlen - 3].close_price < values[vlen - 4].open_price) and
            k_raise(values[vlen - 4])):
            return 32

        #33 == 43
        if (vlen >= 3 and
            fall(values[vlen - 1]) and
            fall(values[vlen - 2]) and
            fall(values[vlen - 3]) and
            values[vlen - 1].lowest_price < values[vlen - 2].lowest_price and
            values[vlen - 2].lowest_price < values[vlen - 3].lowest_price):
            return 33

        #34 == 45
        if (vlen >= 4 and
            (mid_fall(values[vlen - 1]) or big_fall(values[vlen - 1])) and
            small_fall(values[vlen - 2]) and
            small_fall(values[vlen - 3]) and
            small_fall(values[vlen - 4])):
            return 34

        #35 == 47
        if (vlen >= 4 and
            values[vlen - 1].close_price < values[vlen - 2].close_price and
            values[vlen - 2].close_price < values[vlen - 3].close_price and
            values[vlen - 3].close_price < values[vlen - 4].close_price):
            return 35

        #36 == 48
        if (vlen >= 2 and
            big_fall(values[vlen - 1]) and
            far_from(values[vlen - 1].open_price, values[vlen - 2].close_price)):
            return 36

        #37 == 49
        if (vlen >= 4 and
            (cross(values[vlen - 1]) or small_raise(values[vlen - 1]) or small_fall(values[vlen - 1])) and
            (cross(values[vlen - 2]) or small_raise(values[vlen - 2]) or small_fall(values[vlen - 2])) and
            (cross(values[vlen - 3]) or small_raise(values[vlen - 3]) or small_fall(values[vlen - 3])) and
            (mid_fall(values[vlen - 4]) or big_fall(values[vlen - 4])) and
            (max(values[vlen - 1].open_price, values[vlen - 1].close_price) < values[vlen - 4].close_price) and
            (max(values[vlen - 2].open_price, values[vlen - 2].close_price) < values[vlen - 4].close_price) and
            (max(values[vlen - 3].open_price, values[vlen - 3].close_price) < values[vlen - 4].close_price)):
            return 37

        #38 == 50
        if (vlen >= 5 and
            (big_fall(values[vlen - 1]) or mid_fall(values[vlen - 1])) and
            values[vlen - 1].close_price < values[vlen - 4].open_price and
            small_raise(values[vlen - 2]) and values[vlen - 2].close_price > values[vlen - 3].close_price and
            values[vlen - 2].close_price < values[vlen - 5].open_price and
            small_raise(values[vlen - 3]) and values[vlen - 3].close_price > values[vlen - 4].close_price and
            small_raise(values[vlen - 4]) and 
            (big_fall(values[vlen - 5]) or mid_fall(values[vlen - 5]))):
            return 38

        #39 == 52
        if (vlen >= 4 and
            k_raise(values[vlen - 1]) and
            k_raise(values[vlen - 2]) and
            k_raise(values[vlen - 3]) and
            fall(values[vlen - 4]) and
            values[vlen - 3].close_price < values[vlen - 4].close_price and
            values[vlen - 2].close_price < values[vlen - 3].open_price and
            values[vlen - 1].close_price < values[vlen - 2].open_price):
            return 39

        #40 == 53
        if (vlen >= 4 and
            k_raise(values[vlen - 1]) and values[vlen - 1].open_price > values[vlen - 2].close_price and
            k_raise(values[vlen - 2]) and values[vlen - 2].open_price > values[vlen - 3].close_price and
            k_raise(values[vlen - 3]) and values[vlen - 3].open_price > values[vlen - 4].close_price):
            return 40

        #41 == 54
        if (vlen >= 3 and
            k_raise(values[vlen - 1]) and solid(values[vlen - 1]) < solid(values[vlen - 2]) and
            (big_up_shadow(values[vlen - 1]) or mid_up_shadow(values[vlen - 1])) and
            k_raise(values[vlen - 2]) and solid(values[vlen - 2]) < solid(values[vlen - 3]) and
            k_raise(values[vlen - 1])):
            return 41

        #42 == 55
        if (vlen >= 3 and
            k_raise(values[vlen - 1]) and small_solid(values[vlen - 1]) and
            (big_raise(values[vlen - 2]) or mid_raise(values[vlen - 2])) and
            (big_raise(values[vlen - 3]) or mid_raise(values[vlen - 3]))):
            return 42

        #43 == 56
        if (vlen >= 3 and
            k_raise(values[vlen - 1]) and
            k_raise(values[vlen - 2]) and
            k_raise(values[vlen - 3]) and
            values[vlen - 1].close_price < values[vlen - 2].close_price and
            values[vlen - 1].open_price > values[vlen - 2].open_price):
            return 43

        #44 == 57
        if (vlen >= 3 and
            fall(values[vlen - 1]) and
            k_raise(values[vlen - 2]) and
            fall(values[vlen - 3]) and
            values[vlen - 2].close_price < values[vlen - 1].open_price and
            values[vlen - 2].open_price > values[vlen - 1].close_price and
            values[vlen - 2].close_price < values[vlen - 3].open_price and
            values[vlen - 2].open_price > values[vlen - 3].close_price):
            return 44

        #45 == 70
        if (vlen >= 2 and
            fall(values[vlen - 1]) and
            k_raise(values[vlen - 2]) and
            values[vlen - 2].close_price < values[vlen - 1].open_price and
            values[vlen - 2].open_price > values[vlen - 1].close_price):
            return 45

        #46 == 70
        if (vlen >= 2 and
            k_raise(values[vlen - 1]) and
            fall(values[vlen - 2]) and
            values[vlen - 2].open_price < values[vlen - 1].close_price and
            values[vlen - 2].close_price > values[vlen - 1].open_price):
            return 46

        #47 == 69
        if (vlen >= 2 and
            fall(values[vlen - 1]) and
            k_raise(values[vlen - 2]) and
            has_up_shadow(values[vlen - 2]) and
            values[vlen - 1].open_price < values[vlen - 2].highest_price and
            values[vlen - 1].close_price > values[vlen - 2].close_price):
            return 47

        #48 == 69
        if (vlen >= 2 and
            k_raise(values[vlen - 1]) and
            fall(values[vlen - 2]) and
            has_down_shadow(values[vlen - 2]) and
            values[vlen - 1].open_price > values[vlen - 2].lowest_price and
            values[vlen - 1].close_price < values[vlen - 2].close_price):
            return 48

        #49 == 68
        if (vlen >= 2 and
            t_line(values[vlen - 1], True) and
            t_line(values[vlen - 2], False)):
            return 49

        #50 == 68
        if (vlen >= 2 and
            t_line(values[vlen - 1], False) and
            t_line(values[vlen - 2], True)):
            return 49

        #51 == 67
        if (vlen >= 1 and
            t_line(values[vlen - 1], True)):
            return 51

        #52 == 66
        if (vlen >= 1 and
            t_line(values[vlen - 1], False)):
            return 52

        #53 == 65
        if (vlen >= 1 and
            values[vlen - 1].open_price == values[vlen - 1].close_price and
            values[vlen - 1].open_price == values[vlen - 1].lowest_price and
            values[vlen - 1].open_price == values[vlen - 1].highest_price):
            return 53

        #54 == 64
        if (vlen >= 1 and
            fall(values[vlen - 1]) and
            (small_solid(values[vlen - 1]) or mid_solid(values[vlen - 1])) and
            (big_up_shadow(values[vlen - 1]) or mid_up_shadow(values[vlen - 1])) and
            (big_down_shadow(values[vlen - 1]) or mid_down_shadow(values[vlen - 1]))):
            return 54

        #55 == 64
        if (vlen >= 1 and
            k_raise(values[vlen - 1]) and
            (small_solid(values[vlen - 1]) or mid_solid(values[vlen - 1])) and
            (big_up_shadow(values[vlen - 1]) or mid_up_shadow(values[vlen - 1])) and
            (big_down_shadow(values[vlen - 1]) or mid_down_shadow(values[vlen - 1]))):
            return 54

        #56 == 63
        if (vlen >= 1 and
            cross(values[vlen - 1]) and
            (big_up_shadow(values[vlen - 1]) or mid_up_shadow(values[vlen - 1])) and
            (big_down_shadow(values[vlen - 1]) or mid_down_shadow(values[vlen - 1]))):
            return 56

        #57 == 62
        if (vlen >= 1 and
            cross(values[vlen - 1]) and
            (small_up_shadow(values[vlen - 1]) or mid_up_shadow(values[vlen - 1])) and
            (small_down_shadow(values[vlen - 1]) or mid_down_shadow(values[vlen - 1]))):
            return 57

        #58 == 61
        if (vlen >= 1 and
            small_fall(values[vlen - 1])):
            return 58

        #59 == 60
        if (vlen >= 1 and
            small_raise(values[vlen - 1])):
            return 59

        #60 == 59
        if (vlen >= 1 and
            (big_raise(values[vlen - 1]) or mid_raise(values[vlen - 1]))):
            return 60

        #61 == 58
        if (vlen >= 1 and
            (big_fall(values[vlen - 1]) or mid_fall(values[vlen - 1]))):
            return 61

        if (vlen >= 1 and
            fall(values[vlen - 1])):
            return 62
            
        if (vlen >= 1 and
            k_raise(values[vlen - 1])):
            return 63

        if (vlen >= 1 and
            values[vlen - 1].close_price > values[vlen - 1].open_price):
            return 64

        if (vlen >= 1 and
            values[vlen - 1].close_price < values[vlen - 1].open_price):
            return 65

        if (vlen >= 1 and
            values[vlen - 1].close_price == values[vlen - 1].open_price):
            return 66
            
        #No special k line
        return 0

def raise_or_fall_close_on_top_of_prev_close(v1, v2):
    return ((k_raise(v1) and v1.open_price > v2.close_price) or
            (fall(v1) and v1.close_price > v2.close_price))

def k_raise(value):
    return big_raise(value) or mid_raise(value) or small_raise(value)

def fall(value):
    return big_fall(value) or mid_fall(value) or small_fall(value)

def big_raise(value):
    return delta_raise(value, 0.05)

def mid_raise(value):
    return delta_raise(value, 0.03)

def small_raise(value):
    return delta_raise(value, 0.01)

def big_fall(value):
    return delta_fall(value, 0.05)

def mid_fall(value):
    return delta_fall(value, 0.03)

def small_fall(value):
    return delta_fall(value, 0.01)

def delta_raise(value, delta):
    return delta_change(value, delta, True)

def delta_fall(value, delta):
    return delta_change(value, delta, False)

def delta_change(value, delta, go_up):
    if (go_up and value.close_price > value.open_price):
        return value.close_price >= round(value.open_price * (1 + delta))
    elif (not go_up and value.close_price < value.open_price):
        return value.close_price <= round(value.open_price * (1 - delta))
    else:
        return False

def cross(value):
    return (value.lowest_price < value.close_price and
           value.close_price == value.open_price and
           value.highest_price > value.close_price)

def deep_into_3(p, value, delta):
    if (value.open_price < value.close_price):
        return p >= round(delta * (value.close_price - value.open_price) + value.open_price)
    else:
        return p <= round(value.open_price - delta * (value.open_price - value.close_price))

def deep_into(p, value):
    return deep_into_3(p, value, 0.5)

def far_from(p1, p2):
    return far_from_3(p1, p2, 0.05)

def far_from_3(p1, p2, delta):
    return abs(p1 - p2) >= round(min(p1, p2) * delta);

def near_to(p1, p2):
    return near_to_3(p1, p2, 0.01)

def near_to_3(p1, p2, delta):
    return abs(p1 - p2) <= round(min(p1, p2) * delta);

def has_up_shadow(value):
    return big_up_shadow(value) or mid_up_shadow(value) or small_up_shadow(value)

def up_shadow(value):
    v = value.highest_price - max(value.close_price, value.open_price)

    if v > 0:
        return v
    else:
        return 0

def big_up_shadow(value):
    return delta_shadow(value, 0.5, True)

def mid_up_shadow(value):
    return delta_shadow(value, 0.3, True)

def small_up_shadow(value):
    return delta_shadow(value, 0.1, True)

def has_down_shadow(value):
    return big_down_shadow(value) or mid_down_shadow(value) or small_down_shadow(value)

def down_shadow(value):
    v = min(value.close_price , value.open_price) - value.lowest_price

    if v > 0:
        return v
    else:
        return 0

def big_down_shadow(value):
    return delta_shadow(value, 0.5, False)

def mid_down_shadow(value):
    return delta_shadow(value, 0.3, False)

def small_down_shadow(value):
    return delta_shadow(value, 0.1, False)

def delta_shadow(value, delta, up):
    if (up):
        return value.highest_price - max(value.close_price, value.open_price) > round(abs(value.close_price - value.open_price) * delta)
    else:
        return min(value.close_price, value.open_price) - value.lowest_price > round(abs(value.close_price - value.open_price) * delta)

def solid(value):
    return max(value.close_price, value.open_price) - min(value.close_price, value.open_price)

def big_solid(value):
    return delta_solid(value, 0.05)

def mid_solid(value):
    return delta_solid(value, 0.03)

def small_solid(value):
    return delta_solid(value, 0.01)

def delta_solid(value, delta):
    return solid(value) >= round(min(value.close_price, value.open_price) * delta)

def t_line(value, up):
    if up:
        return (value.open_price == value.close_price and
       value.open_price == value.lowest_price and
       value.highest_price > value.open_price)
    else:
        return (value.open_price == value.close_price and
       value.open_price == value.highest_price and
       value.lowest_price < value.open_price)


################ K Line node help functions ############
def create_k_line_node(nm, capacity):
    price_node.create_price_node(nm, capacity)

    _name = "K_Line"

    if not _name in nm.nodes:
        n = KLineNode(nm)
        n.capacity = capacity

        nm.nodes[_name] = n
        return n
    else:
        return nm.nodes[_name]
