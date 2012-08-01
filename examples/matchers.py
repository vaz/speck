import speck
from speck import _

def main():
    _(1).should == 1.0

    x = 1

    _(x).should.be(x)
    _(x).should.be.less_than(1000)
    _(x).should.be_less_than(1000)
    _(x).should.be < 1000
    _(x).should_not.be > 1000
    _(x).should.not_be > 1000
    _(x).should.not_be_greater_than_or_equal(1000)
    _(x).should.not_be_greater_than_or_equal_to(1000)
    _(x).should.not_be('dogs')

    try:
        _(x).should.not_be(x) # raises speck.exception.ExpectationNotMet: NOT 1 is 1
    except speck.exception.ExpectationNotMet:
        pass
    else:
        raise Exception("Expected ExpectationNotMet: NOT 1 is 1")

if __name__ == '__main__':
    main()
