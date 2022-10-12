package agh.ics.oop;

public class World {
    public static void main(String[] args) {
        System.out.println("System wystartowal");
        Direction[] eTab = new Direction[args.length];
        for (int i = 0; i < args.length; i++){
            switch (args[i]){
                case "f" -> eTab[i] = Direction.Forward;
                case "b" -> eTab[i] = Direction.Backward;
                case "r" -> eTab[i] = Direction.Right;
                case "l" -> eTab[i] = Direction.Left;
                default -> eTab[i] = Direction.NONE;
            }
        }
        run(eTab);
        System.out.println("System zakonczyl swoje dzialanie");
    }

    static void run(Direction[] args) {
        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case Forward-> System.out.println("Zwierzak idzie do przodu");
                case Backward -> System.out.println("Zwierzak idzie do tylu");
                case Left -> System.out.println("Zwierzak idzie w lewo");
                case Right -> System.out.println("Zwierzak idzie w prawo");
                default -> System.out.print("");
            }
        }
    }
}
