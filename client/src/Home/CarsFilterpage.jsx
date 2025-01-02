import React, { useEffect, useState } from 'react';
import { useCart } from '../context/cart';
import { Link } from 'react-router-dom';
import '../styles/brands.css';
import { AiOutlineShoppingCart, AiOutlineEye } from 'react-icons/ai';
import { MdAirlineSeatReclineExtra } from 'react-icons/md';
import { BsFuelPumpFill } from 'react-icons/bs';
import { TbStars } from 'react-icons/tb';
import { PiCurrencyInrFill } from 'react-icons/pi';
import toast from 'react-hot-toast';
import { Checkbox, Radio } from 'antd';
import axios from 'axios';
import { Price } from '../pages/Price';
import { ColorRing } from 'react-loader-spinner';

const CarsHome = () => {
    const [cars, setCars] = useState([]);
    const [cart, setCart] = useCart();
    const [brand, setBrand] = useState([]);
    const [selectedBrands, setSelectedBrands] = useState([]);
    const [selectedPriceRange, setSelectedPriceRange] = useState(null);
    const [search, setSearch] = useState('');
    const [loading, setLoading] = useState(true);

    const getAllBrands = async () => {
        try {
            const { data } = await axios.get(`${process.env.REACT_APP_API_URL}/api/v1/brands/all`);
            if (data.success) {
                setBrand(data.data);
            }
            setLoading(false);
        } catch (err) {
            console.error(err);
            setLoading(true);
        }
    };

    const getAllCars = async () => {
        try {
            const { data } = await axios.get(`${process.env.REACT_APP_API_URL}/api/v1/vehicles/all`);
            setCars(data.data.reverse());
            setLoading(false);
        } catch (error) {
            console.error(error);
            setLoading(true);
        }
    };

    const handleBrandChange = (e, brandId) => {
        const isChecked = e.target.checked;
        setSelectedBrands((prev) =>
            isChecked ? [...prev, brandId] : prev.filter((id) => id !== brandId)
        );
    };

    const handlePriceChange = (e) => {
        setSelectedPriceRange(e.target.value);
    };

    const resetFilters = () => {
        setSelectedBrands([]);
        setSelectedPriceRange(null);
        setSearch('');
    };

    const notify = () => toast.success('Added to Cart Successfully');

    useEffect(() => {
        getAllBrands();
        getAllCars();
        window.scrollTo(0, 0);
    }, []);

    // Filtering Logic
    const filteredCars = cars
        .filter((car) =>
            search.toLowerCase() === '' ? true : car.model.toLowerCase().includes(search.toLowerCase())
        )
        .filter((car) =>
            selectedBrands.length === 0 ? true : selectedBrands.includes(car.brand.uuid)
        )
        .filter((car) => {
            if (!selectedPriceRange) return true;
            const [minPrice, maxPrice] = selectedPriceRange;
            console.log(`Car price: ${car.price}, Min price: ${minPrice}, Max price: ${maxPrice}`);

            return car.price >= minPrice && car.price <= maxPrice;
        });

    return (
        <>
            <div className="brand_wrapper" id="cars">
                <div className="col-12 text-center">
                    <p className="brand_subtitle">A Wide Range of Cars Awaits!</p>
                    <h2 className="brand_title">Cars Showcase</h2>
                </div>
            </div>
            <div className="container">
                <div className="row" style={{ marginBottom: '100px', marginTop: '-50px' }}>
                    {/* Sidebar */}
                    <div className="col-md-12 col-lg-3">
                        <h4>🔎 Search Your Car</h4>
                        <div className="input-group d-flex flex-column row">
                            <input
                                type="search"
                                placeholder="🔎 Search your car..."
                                onChange={(e) => setSearch(e.target.value)}
                                className="form-control"
                            />
                        </div>
                        <h4 className="mt-4">Filter By Brands</h4>
                        <div className="d-flex flex-column">
                            {brand.map((b) => (
                                <Checkbox
                                    key={b.uuid}
                                    onChange={(e) => handleBrandChange(e, b.uuid)}
                                    checked={selectedBrands.includes(b.uuid)}
                                >
                                    {b.name}
                                </Checkbox>
                            ))}
                        </div>
                        <h4 className="mt-4">Filter By Price Range</h4>
                        <div className="d-flex flex-column">
                            <Radio.Group onChange={handlePriceChange} value={selectedPriceRange}>
                                {Price.map((p) => (
                                    <Radio key={p.uuid} value={p.array}>
                                        {p.name}
                                    </Radio>
                                ))}
                            </Radio.Group>
                        </div>
                        <button className="btn btn-outline-dark my-4" onClick={resetFilters}>
                            RESET FILTERS
                        </button>
                    </div>

                    {/* Cars Display */}
                    <div className="col-md-12 col-lg-9">
                        {loading ? (
                            <div className="h-100 d-flex align-items-center justify-content-center">
                                <ColorRing
                                    visible={true}
                                    colors={[
                                        '#000435',
                                        'rgb(14 165 233)',
                                        'rgb(243 244 246)',
                                        '#000435',
                                        'rgb(14 165 233)',
                                    ]}
                                />
                            </div>
                        ) : (
                            <div className="row">
                                {filteredCars.map((car) => (
                                    <div className="col-md-12 col-lg-4 mb-3" key={car.uuid}>
                                        <div className="card">
                                            <div className="d-flex justify-content-between p-3">
                                                <p className="lead mb-0 respBrand">{car.brand.name}</p>
                                                <div
                                                    className="rounded-circle d-flex align-items-center justify-content-center shadow-1-strong"
                                                    style={{ width: '35px', height: '35px' }}
                                                >
                                                    <Link
                                                        to={`/brand/${car.brand.slug}`}
                                                        className="text-white mb-0 small"
                                                    >
                                                        <img
                                                            src={car.brand.brandPictures}
                                                            alt={car.brand.name}
                                                            style={{
                                                                maxWidth: '100%',
                                                                maxHeight: '150px',
                                                                objectFit: 'contain',
                                                            }}
                                                        />
                                                    </Link>
                                                </div>
                                            </div>
                                            <Link to={`/car/${car.slug}`} className="text-center">
                                                <img
                                                    src={car.productPictures[0]}
                                                    alt={car.model}
                                                    style={{
                                                        maxWidth: '100%',
                                                        maxHeight: '130px',
                                                        objectFit: 'contain',
                                                    }}
                                                    className="border rounded"
                                                />
                                            </Link>
                                            <div className="card-body">
                                                <h4 className="text-center mb-4 respName">
                                                    {car.model}
                                                </h4>
                                                <div className="d-flex justify-content-between">
                                                    <h6 className="respBrand">
                                                        <PiCurrencyInrFill /> : {car.price} $
                                                    </h6>
                                                    <h6 className="respBrand">
                                                        <BsFuelPumpFill /> : {car.fuelType}
                                                    </h6>
                                                </div>
                                                <div className="d-flex justify-content-between my-2">
                                                    <h6 className="respBrand">
                                                        <TbStars /> : {car.safetyrating}
                                                    </h6>
                                                    <h6 className="respBrand">
                                                        <MdAirlineSeatReclineExtra /> : {car.seater} Seater
                                                    </h6>
                                                </div>
                                                <div className="text-center">
                                                    <Link
                                                        className="btn my-2"
                                                        style={{
                                                            backgroundColor: 'blueviolet',
                                                            color: 'white',
                                                        }}
                                                        to={`/car/${car.slug}`}
                                                    >
                                                        <AiOutlineEye size={20} className="pb-1" /> View
                                                    </Link>
                                                    <button
                                                        className="btn btn-outline-primary my-2 mx-3"
                                                        onClick={() => {
                                                            setCart([...cart, car]);
                                                            localStorage.setItem(
                                                                'cart',
                                                                JSON.stringify([...cart, car])
                                                            );
                                                            notify();
                                                        }}
                                                    >
                                                        <AiOutlineShoppingCart size={20} className="pb-1" />{' '}
                                                        Add To Cart
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </>
    );
};

export default CarsHome;
