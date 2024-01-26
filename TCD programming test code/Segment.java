public class Segment
{
    public static Areas areas(double r, double a) {
        double circleArea = 0.0;
        double segmentArea = 0.0;
        double b = 0.0;
        circleArea = Math.PI * r * r;
        b = Math.PI / 180;
        segmentArea = ((r * r)/2) * (a * b - Math.sin(a * b));
        return new Areas(circleArea, circleArea - segmentArea); // you might change the sequences of 2 arguments 
    }
    
    public static class Areas {
        public final double inside, outside;

        public Areas(double inside, double outside) {         
            this.inside = inside;
            this.outside = outside;
        }
    }
    
    public static void main(String[] args) {
        Areas areas = Segment.areas(10, 90);
        System.out.println("Areas: " + areas.inside + ", " + areas.outside);  
    }
}
