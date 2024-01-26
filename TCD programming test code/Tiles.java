public class Tiles {
    public static void tileEdges(boolean[][] tiles) {
        int rows = tiles.length;
        int cols = tiles[0].length;
        
        for(int col = 0; col < cols; col++) {
            tiles[0][col] = true;      
            tiles[rows-1][col] = true;  
        }

        for(int row = 1; row < rows - 1; row++) {
            tiles[row][0] = true;      
            tiles[row][cols-1] = true;  
        }
    }

    public static void main(String[] args) {
        boolean[][] tiles = new boolean[4][4];
        
        tileEdges(tiles);

        for (int i = 0; i < tiles.length; i++) {
            for (int j = 0; j < tiles[i].length; j++) {
                System.out.print(tiles[i][j] ? "true  " : "false ");
            }
            System.out.println();
        }
    }
}
