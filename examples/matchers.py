from speck import _

"""
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

    _(x).should(x)

if __name__ == '__main__':
    main()
