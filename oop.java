// create a main java class
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello World");
        Int a = 5;
        Int b = 10;

        if (a > b) {
            System.out.println("a is greater than b");
        } else if (a == b) {
            System.out.println("b is greater than a");
        }
        else {
            System.out.println("a is equal to b");
        }
        this.addToNumber(a, b);
        String addToNumber(Int a, Int b){
            return a + b;     
        }

        String addToNumber(Int a, Int b, Int c){
            return a + b + c;     
        }

        Double addToNumber(Double a, Double b){
            return a + b;     
        }
    

    }
}