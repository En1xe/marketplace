import { Card, Collapse, message, Slider, InputNumber } from "antd"
import { useState, useEffect, useCallback } from "react"
import debounce from "lodash/debounce"

import { listingsService } from "@services/api/listings.service"


export default function ListingsFilter({initialListings, setCurrentListings}) {
    const [minPrice, setMinPrice] = useState('')
    const [maxPrice, setMaxPrice] = useState('')
    const [sliderRange, setSliderRange] = useState([0, 0])

    const handleSliderChange = (values) => {
        const [newMin, newMax] = values

        setMinPrice(newMin)
        setMaxPrice(newMax)
        setSliderRange(values)
    }

    const handleMinPriceInputChange = (value) => {
        const [_, maxPrice] = sliderRange

        setMinPrice(value)
        setSliderRange([value, maxPrice])
    }

    const handleMaxPriceInputChange = (value) => {
        const [minPrice, _] = sliderRange
        
        setMaxPrice(value)
        setSliderRange([minPrice, value])
    }

    const maxListingPrice = Math.max(...initialListings.map((item) => item.price))

    const debounceFilter = useCallback(
        debounce(async (minPrice, maxPrice) => {
            const filters = {
                min_price: minPrice || 0,
                max_price: maxPrice || 2147483647,
                is_active: true
            }

            try {
                const filteredListings = await listingsService.getListings(filters)

                if (filteredListings) {
                    setCurrentListings(filteredListings)
                }
            } catch (error) {
                message.error('No listings were received')
            }
        }, 750),
        []
    )

    useEffect(() => {
        if (minPrice === '' && maxPrice === '') return

        debounceFilter(minPrice, maxPrice)

        return () => {
            debounceFilter.cancel()
        }
    }, [minPrice, maxPrice, setCurrentListings])

    return (
        <Card>  
            <ul>
                <li>
                    <Collapse 
                        defaultActiveKey={['price']}
                        bordered={false}
                        items={[{
                            key: 'price',
                            label: 'Prices',
                            children: (
                                <div>
                                    <div className="flex gap-4">
                                        <InputNumber
                                            key='minPrice'
                                            placeholder="0"
                                            suffix='$'
                                            value={minPrice}
                                            onChange={(value) => handleMinPriceInputChange(value)}
                                            min="0"
                                            controls={false}
                                        />
                                        <InputNumber 
                                            key='maxPrice'
                                            placeholder="1000.00"
                                            suffix='$'
                                            value={maxPrice}
                                            onChange={(value) => handleMaxPriceInputChange(value)}
                                            min="0"
                                            controls={false}
                                        />
                                    </div>
                                    <Slider 
                                        range
                                        min={0}
                                        max={maxListingPrice} 
                                        value={sliderRange}
                                        onChange={handleSliderChange}
                                    />
                                </div>
                            )
                        }]}
                    />
                </li>
            </ul>
        </Card>
    )
}