public class BaseClone {
    
    private int test;

    public BaseClone() {
        this.test = 1;
    }

    public BaseClone(int test) {
        this.test = test;
    }

    public void multiply(Base other) {
        test = other.test * test;
    }

    public int challenge(Base other) {
        int returnValue = 0;
        for (int j = 0; j < other.test; j++) {
            returnValue = test + j;
            multiply(other);
        }
        return returnValue;
    }

}
