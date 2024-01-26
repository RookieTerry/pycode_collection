public class CaloriesBurned {
    public static double calculate(int weight, int[][] ride) {
        double result = 0.0;
        double sum = 0.0;
        for(int i = 0; i < ride.length - 1; i++){
            sum += ((2.5 * ride[i][0] - 6) * (ride[i+1][1] - ride[i][1])) / 3600;
        }
        result = sum * weight;
        return result;
    }

    public static void main(String[] args) {
        System.out.println(CaloriesBurned.calculate(60, new int[][]{{6, 0}, {4, 1800}, {0, 3600}})); // should print 390.0
    }
}
