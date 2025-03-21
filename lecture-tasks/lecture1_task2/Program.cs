using System;
using System.Globalization;

namespace lecture1_task2;

class Program
{
    static void CartesianToPolar(double x, double y, uint precision)
    {
        double r = Math.Sqrt(x * x + y * y);

        double thetaInRadians = Math.Atan2(y, x);

        double thetaInDegrees = thetaInRadians * 180 / Math.PI;

        Console.WriteLine($"r = {r.ToString("F" + precision)}, " +
                          $"theta (in degrees) = {thetaInDegrees.ToString("F" + precision)}");
    }

    static void PolarToCartesian(double r, double theta, uint precision)
    {
        double x = r * Math.Cos(theta * Math.PI / 180);

        double y = r * Math.Sin(theta * Math.PI / 180);

        Console.WriteLine($"x = {x.ToString("F" + precision)}, y = {y.ToString("F" + precision)}");
    }

    static void CartesianToSpherical(double x, double y, uint precision, double z = 0)
    {
        double r = Math.Sqrt(x * x + y * y + z * z);

        double thetaInRadians = Math.Acos(z / r);
        
        double thetaInDegrees = thetaInRadians * 180 / Math.PI;

        double phiInRadians = Math.Atan2(y, x);
        
        double phiInDegrees = phiInRadians * 180 / Math.PI;

        Console.WriteLine($"r = {r.ToString("F" + precision)}, " +
                          $"theta (in degrees) = {thetaInDegrees.ToString("F" + precision)}, " +
                          $"phi (in degrees) = {phiInDegrees.ToString("F" + precision)}");
    }

    static void SphericalToCartesian(double r, double theta, double phi, uint precision)
    {
        double thetaInRadians = theta * Math.PI / 180;

        double phiInRadians = phi * Math.PI / 180;

        double x = r * Math.Sin(thetaInRadians) * Math.Cos(phiInRadians);
        
        double y = r * Math.Sin(thetaInRadians) * Math.Sin(phiInRadians);
        
        double z = r * Math.Cos(thetaInRadians);

        Console.WriteLine($"x = {x.ToString("F" + precision)}, " +
                          $"y = {y.ToString("F" + precision)}, " +
                          $"y = {z.ToString("F" + precision)}");
    }

    static void CartesianToCylindrical(double x, double y, uint precision, double z = 0)
    {
        double r = Math.Sqrt(x * x + y * y);

        double thetaInRadians = Math.Atan2(y, x);

        double thetaInDegrees = thetaInRadians * 180 / Math.PI;

        double height = z;

        Console.WriteLine($"r = {r.ToString("F" + precision)}, " +
                          $"theta (in degrees) = {thetaInDegrees.ToString("F" + precision)}, " +
                          $"z = {height.ToString("F" + precision)}");
    }

    static void CylindricalToCartesian(double r, double theta, double height, uint precision)
    {
        double thetaInRadians = theta * Math.PI / 180;

        double x = r * Math.Cos(thetaInRadians);
        
        double y = r * Math.Sin(thetaInRadians);

        double z = height;
        
        Console.WriteLine($"x = {x.ToString("F" + precision)}, " +
                          $"y = {y.ToString("F" + precision)}, " +
                          $"z = {z.ToString("F" + precision)}");
    }

    static void Main(string[] args)
    {
        while (true)
        {
            NumberFormatInfo numberFormatInfo = new NumberFormatInfo()
            {
                NumberDecimalSeparator = ".",
            };

            uint convertFrom = 0;
            while (!(new uint[] { 1, 2, 3, 4 }).Contains(convertFrom))
            {
                Console.WriteLine("Choose the coordinate system to convert from: ");
                Console.WriteLine("1: Cartesian");
                Console.WriteLine("2: Polar");
                Console.WriteLine("3: Spherical");
                Console.WriteLine("4: Cylindrical");
                convertFrom = uint.Parse(Console.ReadLine());
            }

            uint convertTo = 0;
            while (!(new uint[] { 1, 2, 3, 4 }).Contains(convertTo))
            {
                Console.WriteLine("Choose the coordinate system to convert to: ");
                Console.WriteLine("1: Cartesian");
                Console.WriteLine("2: Polar");
                Console.WriteLine("3: Spherical");
                Console.WriteLine("4: Cylindrical");
                convertTo = uint.Parse(Console.ReadLine());
            }

            switch (convertFrom)
            {
                case 1:
                {
                    Console.WriteLine("Enter x");
                    var x = double.Parse(Console.ReadLine(), numberFormatInfo);
                    Console.WriteLine("Enter y");
                    var y = double.Parse(Console.ReadLine(), numberFormatInfo);
                    Console.WriteLine("Set precision");
                    var precision = uint.Parse(Console.ReadLine());

                    switch (convertTo)
                    {
                        case 2:
                            CartesianToPolar(x, y, precision);
                            break;
                        case 3:
                            CartesianToSpherical(x, y, precision);
                            break;
                        case 4:
                            CartesianToCylindrical(x, y, precision);
                            break;
                        default:
                            Console.WriteLine($"x = {x}, y = {y}");
                            break;
                    }

                    break;
                }

                case 2:
                {
                    Console.WriteLine("Enter r");
                    var r = double.Parse(Console.ReadLine(), numberFormatInfo);
                    Console.WriteLine("Enter theta (in degrees)");
                    var theta = double.Parse(Console.ReadLine(), numberFormatInfo);
                    Console.WriteLine("Set precision");
                    var precision = uint.Parse(Console.ReadLine());

                    switch (convertTo)
                    {
                        case 1:
                            PolarToCartesian(r, theta, precision);
                            break;
                        default:
                            Console.WriteLine($"r = {r}, theta (in degrees) = {theta}");
                            break;
                    }

                    break;
                }

                case 3:
                {
                    Console.WriteLine("Enter r");
                    var r = double.Parse(Console.ReadLine(), numberFormatInfo);
                    Console.WriteLine("Enter theta (in degrees)");
                    var theta = double.Parse(Console.ReadLine(), numberFormatInfo);
                    Console.WriteLine("Enter phi (in degrees)");
                    var phi = double.Parse(Console.ReadLine(), numberFormatInfo);
                    Console.WriteLine("Set precision");
                    var precision = uint.Parse(Console.ReadLine());
                    
                    switch (convertTo)
                    {
                        case 1:
                            SphericalToCartesian(r, theta, phi, precision);
                            break;
                        default:
                            Console.WriteLine($"r = {r}, theta (in degrees) = {theta}, phi (in degrees) = {phi}");
                            break;
                    }

                    break;
                }

                case 4:
                {
                    Console.WriteLine("Enter r");
                    var r = double.Parse(Console.ReadLine(), numberFormatInfo);
                    Console.WriteLine("Enter theta (in degrees)");
                    var theta = double.Parse(Console.ReadLine(), numberFormatInfo);
                    Console.WriteLine("Enter height");
                    var height = double.Parse(Console.ReadLine(), numberFormatInfo);
                    Console.WriteLine("Set precision");
                    var precision = uint.Parse(Console.ReadLine());
                    
                    switch (convertTo)
                    {
                        case 1:
                            CylindricalToCartesian(r, theta, height, precision);
                            break;
                        default:
                            Console.WriteLine($"r = {r}, theta (in degrees) = {theta}, height = {height}");
                            break;
                    }

                    break;
                }
            }
        }
    }
}