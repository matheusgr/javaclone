public class BaseClone {
    
    private int test;

    public BaseClone() {
        this(1);
    }

    public BaseClone(int test) {
        this.test = test;
    }

    public void multiply(BaseClone other) {
        this.test *= other.test;
    }

    public int challenge(BaseClone other) {
        int returnValue = 0;
        for (int i = 0; i < other.test; i++) {
            multiply(other);
            returnValue = this.test + i;
        }
        return returnValue;
    }

}
