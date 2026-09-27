package lab;

import com.amazonaws.athena.connector.lambda.handlers.UserDefinedFunctionHandler;

/** Scalar UDFs for the dbt Athena adapter tests. Athena calls the lowercase public methods by name. */
public class LabUdfHandler extends UserDefinedFunctionHandler
{
    public LabUdfHandler()
    {
        super("lab_udf");
    }

    public String lab_upper(String input)
    {
        return input == null ? null : input.toUpperCase();
    }

    public Integer lab_add(Integer a, Integer b)
    {
        return (a == null || b == null) ? null : a + b;
    }
}
