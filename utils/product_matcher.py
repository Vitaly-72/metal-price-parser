from typing import List, Dict

class ProductMatcher:
    @staticmethod
    def match_products(trimet_products: List[Dict], parad_products: List[Dict]) -> List[Dict]:
        matched_products = []
        
        print(f"Matching {len(trimet_products)} Trimet products with {len(parad_products)} Parad products")
        
        for t_product in trimet_products:
            matched = False
            for p_product in parad_products:
                if (t_product['diameter'] == p_product['diameter'] and 
                    abs(t_product['length'] - p_product['length']) < 0.1 and
                    t_product['diameter'] is not None and 
                    p_product['diameter'] is not None):
                    
                    matched_products.append({
                        'name': f"Арматура {t_product['diameter']} {t_product['length']}м",
                        'diameter': t_product['diameter'],
                        'length': t_product['length'],
                        'prices': {
                            'Тримет': t_product['price'],
                            'Парад': p_product['price']
                        },
                        'trimet_original': t_product['original_name'],
                        'parad_original': p_product['original_name']
                    })
                    matched = True
                    print(f"Matched: {t_product['normalized_name']} -> {p_product['normalized_name']}")
                    break
            
            if not matched:
                print(f"No match for: {t_product['normalized_name']}")
        
        return matched_products
