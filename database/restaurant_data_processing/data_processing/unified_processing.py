def unify_data(df_shopee, df_google):
    return df_shopee.unionByName(df_google, allowMissingColumns=True)