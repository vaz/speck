from speck import _

"""
ideas:

x = _(expr)

x.should == 5
x.should.equal(5)
x.should_not == 5
x.should_not.equal(5)
x.should != 5
x.should.not_equal(5)
x.should_not != 5
x.should_not.not_equal(5)

x.should < 5
x.should.be < 5
x.should.be.not_equal(5)
x.should.be.not_less_than(5)

x.should.be(5)

x.should.be.true
x.should.be.false
x.should.be.none (nil, null)

x.should.be_true
x.should.be_false
x.should.be_none (be_nil, be_null)

x.should.be.kind_of(int)
x.should.be.instance_of(int)
x.should.be.kindof(int)
x.should.be.instanceof(int)

x.should.be.even

x.should.have(5).items
x.should.have(5).things
x.should.have < 5
x.should.contain < 5
x.should.have_length < 5
x.should.have.less_than(5).things
x.should.contain(5).things

"""

def main():
    _(1).should == 1.0

    x = 1

    _(x).should.be(x)
    _(x).should.be.less_than(1000)
    _(x).should.be_less_than(1000)
    _(x).should.be < 1000
    _(x).should < 1000 # not as nice but works
    _(x).should_not > 1000
    _(x).should_not.be > 1000
    _(x).should.not_be > 1000
    _(x).should.not_be_greater_than_or_equal(1000)
    _(x).should.not_be_greater_than_or_equal_to(1000)
    _(x).should.not_be('dogs')
    _(x).should.not_be(x) # raises speck.exception.ExpectationNotMet: NOT 1 is 1

if __name__ == '__main__':
    main()
