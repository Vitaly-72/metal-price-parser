from typing import List, Dict

class ProductMatcher:
    @staticmethod
    def match_products(trimet_products: List[Dict], parad_products: List[Dict]) -> List[Dict]:
        matched_products = []
        
        for t_product in trimet_products:
            for p_product in parad_products:
                if (t_product['diameter'] == p_product['diameter'] and 
                    t_product['length'] == p_product['length'] and
                    t_product['diameter'] is not None and 
                    p_product['diameter'] is not None):
                    
                    matched_products.append({
                        'name': f"Арматура {t_product['diameter']} {t_product['length']}м",
                        'diameter': t_product['diameter'],
                        'length': t_product['length'],
                        'prices': {
                            'Тримет': t_product['price'],
                            'Парад': p_product['price']
                        }
                    })
                    break
        
        return matched_products
